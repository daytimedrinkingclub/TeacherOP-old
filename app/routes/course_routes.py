import json
import logging

from flask import jsonify, request, url_for
from flask_socketio import emit

from ..models.course_models import Course
from ..services.ai_service import AiService
from ..socketio_config import socketio
from . import course_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@course_bp.route("/create", methods=["POST"])
def create_course():
    logging.info("create_course route called from client")
    data = request.get_json()
    logging.info(f"Received data: {data}")
    query = data.get("query")
    if query:
        try:
            logging.info("Query found, passing query to AI function")
            response = AiService.generate_onboarding_question(query)
            if response and isinstance(response, list) and len(response) > 0:
                text_block = response[0]
                response_data = json.loads(text_block.text)
                logging.info(f"AI response data: {response_data}")

                if "tool_use" in response_data:
                    tool_use = response_data["tool_use"]
                    tool_name = tool_use["name"]
                    tool_input = tool_use["input"]
                    logging.info(f"Tool name: {tool_name}")
                    logging.info(f"Tool input: {tool_input}")

                    if tool_name == "get_user_data":
                        question_format = tool_input["question_format"]
                        question_text = tool_input["question_text"]
                        answer_type = tool_input["answer_type"]
                        answer_values = tool_input["answer_values"]

                        socket_url = url_for("socketio.init_socketio", _external=True)
                        return jsonify({"socketUrl": socket_url}), 200

                    elif tool_name == "generate_plan_summary":
                        plan_overview = tool_input["plan_overview"]
                        learning_goal = tool_input["learning_goal"]
                        deadline = tool_input["deadline"]
                        current_skill_level = tool_input["current_skill_level"]

                        socket_url = url_for("socketio.init_socketio", _external=True)
                        logging.info(f"Socket URL: {socket_url}")
                        return jsonify({"socketUrl": socket_url}), 200
                else:
                    socket_url = url_for("socketio.init_socketio", _external=True)
                    logging.info(f"Default socket URL: {socket_url}")
                    return jsonify({"socketUrl": socket_url}), 200
            else:
                logging.error("Invalid response format")
                return jsonify({"message": "Invalid response format"}), 400
        except Exception as e:
            logging.error(f"Error in create_course route: {e}")
            return jsonify({"message": str(e)}), 500
    else:
        logging.warning("No query provided")
        return jsonify({"message": "No query provided"}), 400


@socketio.on("answerQuestion")
def handle_answer_question(data):
    logging.info("answerQuestion route called from client")
    answer = data.get("answer")
    if answer:
        try:
            response = AiService.generate_onboarding_question(conversation=answer)
            if response and isinstance(response, list) and len(response) > 0:
                text_block = response[0]
                response_data = json.loads(text_block.text)

                if "tool_use" in response_data:
                    tool_use = response_data["tool_use"]
                    tool_name = tool_use["name"]
                    tool_input = tool_use["input"]

                    if tool_name == "get_user_data":
                        question_format = tool_input["question_format"]
                        question_text = tool_input["question_text"]
                        answer_type = tool_input["answer_type"]
                        answer_values = tool_input["answer_values"]

                        emit(
                            "questionReceived",
                            {
                                "question_format": question_format,
                                "question_text": question_text,
                                "answer_type": answer_type,
                                "answer_values": answer_values,
                            },
                        )
                    elif tool_name == "generate_plan_summary":
                        plan_overview = tool_input["plan_overview"]
                        learning_goal = tool_input["learning_goal"]
                        deadline = tool_input["deadline"]
                        current_skill_level = tool_input["current_skill_level"]

                        emit(
                            "summaryReceived",
                            {
                                "plan_overview": plan_overview,
                                "learning_goal": learning_goal,
                                "deadline": deadline,
                                "current_skill_level": current_skill_level,
                            },
                        )
                else:
                    emit("summaryReceived", response_data)
            else:
                emit("error", {"message": "Invalid response format"})
        except Exception as e:
            emit("error", {"message": str(e)})
    else:
        emit("error", {"message": "No answer provided"})


@course_bp.route("/courses", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    return jsonify(courses), 200
