from flask import request, jsonify
from . import bp  # import the Blueprint instance
from .util import sendMail


@bp.route("/contact_team", methods=["POST"])
async def contact_team():
    data = request.json  # Get JSON data from frontend
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")
    subject = data.get("subject")

    if not all([name, email, message, subject]):
        return jsonify({"error": "All fields are required"}), 400
    if not isinstance(name, str) or not isinstance(email, str) or not isinstance(message, str) or not isinstance(subject, str):
        return jsonify({"error": "Invalid data type"}), 400
    
    html_content = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #2c3e50;">Hello, {name}</h2>
        <h3>We have received your message:</h3>
        <p style="font-size: 18px; font-weight: bold; color: #27ae60;">"{message}"</p>
        <p>We will get back to you as soon as possible.</p>
         <img src="https://dxm.content-center.totalenergies.com/api/wedia/dam/transform/xysh7dg731tahpw133wmjuk8by/roadside-vehicle-repair-service-workers-change-mount-tires-garage-car-341509-3419-jpeg.webp?option=default" 
             alt="Car Service" style="width:100%; max-width:600px; margin-top:20px; border-radius:8px;" />
        <p style="color: #95a5a6; font-size: 12px;">CarEase Team</p>
        <p style="color: #95a5a6; font-size: 12px;">This is an automated message, please do not reply.</p>
    </div>
    """
    try:
        await sendMail(email, subject, html_content)
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    pass

