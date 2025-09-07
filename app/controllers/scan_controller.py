from crypt import methods
from email import message
from flask import Blueprint, request, jsonify
from typing import Dict, Any
from app.services.scan_service import ScanService
from app.schemas.scan_dtos import PortScanRequest, FastScanRequest
from app.schemas.response_dtos import SuccessResponse, ErrorResponse
from app.utils.logger import controller_logger, log_function_entry, log_function_exit
from pydantic import ValidationError


scan_bp=Blueprint('scan', __name__,url_prefix='/api/v2/scan')

scan_service=ScanService()

@scan_bp.route("/ports",methods=['POST'])
def create_port_scan():
    log_function_entry(controller_logger,"create_port_scan")
    try:
        controller_logger.info("Parsing request data....")
        data=request.get_json()

        if not data:
            controller_logger.error("No data provided")
            return jsonify(ErrorResponse(
                message="JSON Data required",
                error_code="NO_DATA"
            ).dict()),400

        controller_logger.info(f"Validating request data {data}")

        # Pydantic validation
        controller_logger.info("🔍 Validating request...")
        try:
            scan_request = PortScanRequest(**data)
            controller_logger.info(f"✅ Validation passed: {scan_request.target}")
        except ValidationError as e:
            controller_logger.error(f"❌ Validation failed: {e}")
            return jsonify(ErrorResponse(
                message="Validation failed",
                error_code="VALIDATION_ERROR",
                details=e.errors()
            ).dict()), 400

        controller_logger.info("Calling scan service....")
        result=scan_service.create_port_scan(scan_request)

        controller_logger.info("Scan service completed successfully")

        # 4. Response döner
        response = SuccessResponse(
            message=f"Port scan completed for {scan_request.target}",
            data=result
        )
        
        log_function_exit(controller_logger, "create_port_scan", "SuccessResponse")
        return jsonify(response.dict()), 200

    except Exception as e:
        controller_logger.error(f"💥 Unexpected error: {str(e)}")
        error_response = ErrorResponse(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            details={"error": str(e)}
        )
        return jsonify(error_response.dict()), 500

@scan_bp.route('/fast', methods=['POST'])
def create_fast_scan():
    """Fast scan endpoint"""
    log_function_entry(controller_logger, "create_fast_scan")
    
    try:
        # 1. Request al
        controller_logger.info("📨 Processing fast scan request...")
        data = request.get_json()
        
        if not data:
            return jsonify(ErrorResponse(
                message="JSON data required",
                error_code="NO_DATA"
            ).dict()), 400
        
        # 2. Validate
        controller_logger.info("🔍 Validating fast scan request...")
        try:
            scan_request = FastScanRequest(**data)
            controller_logger.info(f"✅ Fast scan validation passed: {scan_request.target}")
        except ValidationError as e:
            controller_logger.error(f"❌ Fast scan validation failed: {e}")
            return jsonify(ErrorResponse(
                message="Validation failed",
                error_code="VALIDATION_ERROR",
                details=e.errors()
            ).dict()), 400
        
        # 3. Service çağır
        controller_logger.info(f"⚡ Starting fast scan: {scan_request.start_port}-{scan_request.end_port}")
        result = scan_service.create_fast_scan(scan_request)
        controller_logger.info(f"🎯 Fast scan completed: {len(result['open_ports'])} ports found")
        
        # 4. Response
        response = SuccessResponse(
            message=f"Fast scan completed for {scan_request.target}",
            data=result
        )
        
        log_function_exit(controller_logger, "create_fast_scan", "SuccessResponse")
        return jsonify(response.dict()), 200
        
    except Exception as e:
        controller_logger.error(f"💥 Fast scan error: {str(e)}")
        return jsonify(ErrorResponse(
            message="Fast scan failed",
            error_code="SCAN_ERROR",
            details={"error": str(e)}
        ).dict()), 500

@scan_bp.route('/history', methods=['GET'])
def get_scan_history():
    """Get scan history"""
    log_function_entry(controller_logger, "get_scan_history")
    
    try:
        # Query parameters
        limit = request.args.get('limit', 10, type=int)
        controller_logger.info(f"📊 Fetching scan history, limit: {limit}")
        
        # Service çağır
        scans = scan_service.get_scan_history(limit)
        controller_logger.info(f"✅ Found {len(scans)} scans in history")
        
        response = SuccessResponse(
            message=f"Retrieved {len(scans)} scans",
            data={'scans': scans, 'count': len(scans)}
        )
        
        log_function_exit(controller_logger, "get_scan_history", f"{len(scans)} scans")
        return jsonify(response.dict()), 200
        
    except Exception as e:
        controller_logger.error(f"💥 History fetch error: {str(e)}")
        return jsonify(ErrorResponse(
            message="Failed to fetch scan history",
            error_code="FETCH_ERROR"
        ).dict()), 500

@scan_bp.route('/<int:scan_id>', methods=['GET'])
def get_scan_by_id(scan_id: int):
    """Get specific scan by ID"""
    log_function_entry(controller_logger, "get_scan_by_id", scan_id=scan_id)
    
    try:
        controller_logger.info(f"🔍 Looking for scan ID: {scan_id}")
        
        # Service'den scan al
        scan_data = scan_service.get_scan_by_id(scan_id)
        
        if not scan_data:
            controller_logger.warning(f"⚠️  Scan not found: {scan_id}")
            return jsonify(ErrorResponse(
                message=f"Scan {scan_id} not found",
                error_code="NOT_FOUND"
            ).dict()), 404
        
        controller_logger.info(f"✅ Scan found: {scan_data['scan']['target_ip']}")
        
        response = SuccessResponse(
            message=f"Scan {scan_id} retrieved",
            data=scan_data
        )
        
        log_function_exit(controller_logger, "get_scan_by_id", "ScanData")
        return jsonify(response.dict()), 200
        
    except Exception as e:
        controller_logger.error(f"💥 Scan fetch error: {str(e)}")
        return jsonify(ErrorResponse(
            message="Failed to fetch scan",
            error_code="FETCH_ERROR"
        ).dict()), 500

@scan_bp.route('/stats', methods=['GET'])
def get_scan_statistics():
    """Get scan statistics"""
    log_function_entry(controller_logger, "get_scan_statistics")
    
    try:
        controller_logger.info("📈 Calculating scan statistics...")
        
        # Service'den istatistikleri al
        stats = scan_service.get_scan_statistics()
        controller_logger.info(f"✅ Statistics ready: {stats['total_scans']} total scans")
        
        response = SuccessResponse(
            message="Scan statistics retrieved",
            data=stats
        )
        
        log_function_exit(controller_logger, "get_scan_statistics", "Statistics")
        return jsonify(response.dict()), 200
        
    except Exception as e:
        controller_logger.error(f"💥 Statistics error: {str(e)}")
        return jsonify(ErrorResponse(
            message="Failed to fetch statistics",
            error_code="STATS_ERROR"
        ).dict()), 500

# Health check endpoint
@scan_bp.route('/health', methods=['GET'])
def health_check():
    """Scan service health check"""
    controller_logger.info("🩺 Health check requested")
    
    try:
        # Basit bir test
        stats = scan_service.get_scan_statistics()
        
        response = SuccessResponse(
            message="Scan service is healthy",
            data={
                'status': 'healthy',
                'service': 'scan_controller',
                'total_scans': stats['total_scans']
            }
        )
        
        controller_logger.info("✅ Health check passed")
        return jsonify(response.dict()), 200
        
    except Exception as e:
        controller_logger.error(f"💥 Health check failed: {str(e)}")
        return jsonify(ErrorResponse(
            message="Scan service unhealthy",
            error_code="HEALTH_CHECK_FAILED"
        ).dict()), 503