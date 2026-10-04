"""
ACT-TREE 360 FastAPI Application & HITL Web Interface
Author: Om Mishra (Electronics Engineering 3rd Year, IIT BHU)
"""

import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from app.schemas.events import StreamEvent
from app.hitl.service import HITLService
from app.observability.audit import AuditLogger

app = FastAPI(
    title="ACT-TREE 360 — Proactive Intervention Desk API",
    version="2.0.0",
    description="Ambient Multi-Agent Customer 360 & Dynamic Life-Phase Hypothesis Tree Engine"
)

hitl_service = HITLService()
audit_logger = AuditLogger()


@app.get("/", response_class=HTMLResponse)
async def dashboard_home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>ACT-TREE 360 — Proactive Intervention Desk</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
            .container { max-width: 900px; margin: 0 auto; background: #1e293b; border-radius: 12px; padding: 24px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
            h1 { color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 12px; }
            .card { background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 16px; margin-bottom: 20px; }
            .badge { display: inline-block; padding: 4px 12px; border-radius: 9999px; font-weight: bold; font-size: 0.85rem; }
            .badge-high { background-color: #ef4444; color: white; }
            .badge-medium { background-color: #f59e0b; color: white; }
            .badge-low { background-color: #10b981; color: white; }
            .signal-list { list-style-type: none; padding-left: 0; }
            .signal-list li { padding: 6px 0; color: #cbd5e1; }
            .signal-list li::before { content: "✓ "; color: #38bdf8; font-weight: bold; }
            .btn { padding: 10px 20px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; margin-right: 10px; }
            .btn-approve { background-color: #10b981; color: white; }
            .btn-reject { background-color: #ef4444; color: white; }
            .btn-modify { background-color: #3b82f6; color: white; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ ACT-TREE 360 — Proactive Intervention Desk</h1>
            <p><strong>System Status:</strong> <span style="color: #10b981;">● Online & Monitoring Stream</span></p>
            
            <div class="card">
                <h2>👤 CUSTOMER PROFILE: Marcus Vance (CUST_00042)</h2>
                
                <p><strong>Inferred Life Phase:</strong> Medical Hardship <span class="badge badge-high">Conf: 95%</span></p>
                <p><strong>Churn Risk:</strong> LOW <span class="badge badge-low">12%</span></p>
                
                <h3>Active Evidence Signals:</h3>
                <ul class="signal-list">
                    <li>Hospital Bill Posted ($500.00, ER Visit)</li>
                    <li>Short-Term Disability Income Credit (Benefits replacing salary)</li>
                    <li>Hardship Search Query ("medical hardship payment plan")</li>
                    <li>Support Chat Transcript ("I've been in hospital, need payment plan")</li>
                    <li>Red-Herring Transfer Audited (Tuition wire $12,000 isolated)</li>
                </ul>

                <h3>Recommended Action:</h3>
                <p style="font-size: 1.2rem; color: #38bdf8; font-weight: bold;">Support Intervention: Medical Hardship Payment Plan</p>

                <p><strong>Estimated Cost:</strong> ₹0</p>
                <p><strong>Policy Citation:</strong> [POL_001_MEDICAL_HARDSHIP] Medical Hardship Assistance & Fee Waiver Policy</p>

                <div style="margin-top: 20px;">
                    <button class="btn btn-approve" onclick="alert('Action Approved')">APPROVE</button>
                    <button class="btn btn-reject" onclick="alert('Action Rejected')">REJECT</button>
                    <button class="btn btn-modify" onclick="alert('Modify Action')">MODIFY</button>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "system": "ACT-TREE 360", "version": "2.0.0"}
