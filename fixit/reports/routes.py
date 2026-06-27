from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from fixit.reports.models import Report, VALID_TARGET_TYPES

ns = Namespace('reports', description='Report operations')

report_model = ns.model('Report', {
    'target_id': fields.String(required=True),
    'target_type': fields.String(required=True),
    'reason': fields.String(required=True)
})

@ns.route('/')
class ReportList(Resource):
    @jwt_required()
    @ns.expect(report_model)
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.json

        existing = Report.query.filter_by(
            reporter_id=current_user_id,
            target_id=data['target_id']
        ).first()
        if existing:
            return {'error': 'You have already reported this'}, 400

        try:
            report = Report(
                reporter_id=current_user_id,
                target_id=data['target_id'],
                target_type=data['target_type'],
                reason=data['reason']
            )
            report.save()
            return report.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    def get(self):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin access required'}, 403

        reports = Report.query.all()
        return [r.to_dict() for r in reports], 200

@ns.route('/<string:report_id>/resolve')
class ReportResolve(Resource):
    @jwt_required()
    def put(self, report_id):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin access required'}, 403

        report = Report.query.get(report_id)
        if not report:
            return {'error': 'Report not found'}, 404

        report.resolved = True
        report.update()
        return report.to_dict(), 200
