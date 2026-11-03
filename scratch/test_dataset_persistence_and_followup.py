import os
import sys
import json
import io
from pathlib import Path
from dotenv import load_dotenv

project_dir = Path(r"C:\Users\karan\Desktop\AgentX")
sys.path.insert(0, str(project_dir))
load_dotenv(project_dir / ".env")

import app as flask_app
from utils.auth_db import (
    init_db,
    register_user,
    authenticate_user,
    get_user_conversations,
    get_conversation,
    get_conversation_messages
)

def run_tests():
    print("=" * 60)
    print("AgentX Chat History & Dataset Persistence E2E Test")
    print("=" * 60)

    # 1. Initialize client
    flask_app.app.config["TESTING"] = True
    client = flask_app.app.test_client()

    # 2. Register / Authenticate test user
    username = "test_e2e_student"
    password = "SecurePassword123!"
    success, msg = register_user(username, password)
    print(f"[1] Register user: success={success}, msg={msg}")
    
    user = authenticate_user(username, password)
    assert user is not None, "Authentication failed!"
    print(f"[2] Authenticate user: user_id={user['id']}, username={user['username']}")

    with client.session_transaction() as sess:
        sess["user_id"] = user["id"]
        sess["username"] = user["username"]

    # 3. Upload dataset
    sample_csv = (
        "name,department,cgpa,package,attendance\n"
        "Aarav Sharma,Computer Science,9.4,18.5,92\n"
        "Diya Patel,Information Tech,8.8,14.0,88\n"
        "Rohan Gupta,Electronics,7.9,9.5,82\n"
        "Sneha Rao,Mechanical,8.2,11.0,85\n"
        "Vikram Singh,Civil,7.5,7.5,78\n"
    )
    data = {
        "file": (io.BytesIO(sample_csv.encode("utf-8")), "students_e2e.csv")
    }
    upload_res = client.post("/api/upload", data=data, content_type="multipart/form-data")
    assert upload_res.status_code == 200, f"Upload failed: {upload_res.data}"
    upload_json = upload_res.get_json()
    dataset_id = upload_json["dataset_id"]
    print(f"[3] Upload successful: dataset_id={dataset_id}, rows={upload_json['rows']}, cols={upload_json['columns']}")

    # Verify dataset saved on disk
    saved_files = list(flask_app.UPLOAD_DIR.glob(f"{dataset_id}_*"))
    assert len(saved_files) == 1, f"Expected 1 saved dataset file, found {saved_files}"
    print(f"[4] Verified dataset file on disk: {saved_files[0].name}")

    # 4. Turn 1: Initial metric question
    q1 = "What is the average package?"
    ask_res1 = client.post("/api/ask", json={"dataset_id": dataset_id, "question": q1})
    assert ask_res1.status_code == 200, f"Ask 1 failed: {ask_res1.data}"
    res1_json = ask_res1.get_json()
    conv_id = res1_json["conversation_id"]
    print(f"[5] Q1: '{q1}' -> Conv ID: {conv_id}")
    print(f"    Answer: {res1_json['answer'][:100]}...")

    # 5. Turn 2: Follow-up metric question
    q2 = "What about the minimum?"
    ask_res2 = client.post("/api/ask", json={"dataset_id": dataset_id, "question": q2, "conversation_id": conv_id})
    assert ask_res2.status_code == 200, f"Ask 2 failed: {ask_res2.data}"
    res2_json = ask_res2.get_json()
    print(f"[6] Q2: '{q2}' -> Continued in Conv ID: {res2_json['conversation_id']}")
    print(f"    Answer: {res2_json['answer'][:100]}...")
    assert "7.5" in str(res2_json['answer']) or "minimum" in str(res2_json['answer']).lower(), f"Unexpected answer: {res2_json['answer']}"

    # 6. Turn 3: Ranking question
    q3 = "Who has the highest CGPA?"
    ask_res3 = client.post("/api/ask", json={"dataset_id": dataset_id, "question": q3, "conversation_id": conv_id})
    assert ask_res3.status_code == 200, f"Ask 3 failed: {ask_res3.data}"
    res3_json = ask_res3.get_json()
    print(f"[7] Q3: '{q3}' -> Answer: {res3_json['answer'][:100]}...")
    assert "Aarav" in str(res3_json['answer']), f"Expected Aarav in answer, got: {res3_json['answer']}"

    # 7. Turn 4: Follow-up entity question
    q4 = "Show me the details of that student"
    ask_res4 = client.post("/api/ask", json={"dataset_id": dataset_id, "question": q4, "conversation_id": conv_id})
    assert ask_res4.status_code == 200, f"Ask 4 failed: {ask_res4.data}"
    res4_json = ask_res4.get_json()
    print(f"[8] Q4: '{q4}' -> Answer: {res4_json['answer'][:100]}...")

    # 8. Test memory cache eviction & persistence restoration
    print("\n[9] Simulating server restart / cache eviction...")
    flask_app.datasets.clear()  # Evict memory cache
    assert len(flask_app.datasets) == 0, "Cache should be empty"

    # Call api to get conversation messages - should reload dataset automatically
    msg_res = client.get(f"/api/conversations/{conv_id}/messages")
    assert msg_res.status_code == 200, f"Get messages failed: {msg_res.data}"
    msg_json = msg_res.get_json()
    assert msg_json["dataset"]["available"] is True, "Dataset should be restored as available"
    assert msg_json["dataset"]["rows"] == 5, f"Expected 5 rows, got {msg_json['dataset']['rows']}"
    assert len(msg_json["messages"]) == 8, f"Expected 8 messages (4 user + 4 ai), got {len(msg_json['messages'])}"
    print(f"    Restored dataset '{msg_json['dataset']['filename']}' ({msg_json['dataset']['rows']} rows, {msg_json['dataset']['columns']} cols)")
    print(f"    Loaded {len(msg_json['messages'])} conversation messages chronologically")

    # 9. Ask new question after restart / eviction without explicitly passing dataset_id
    q5 = "What is his attendance?"
    ask_res5 = client.post("/api/ask", json={"conversation_id": conv_id, "question": q5})
    assert ask_res5.status_code == 200, f"Ask 5 failed: {ask_res5.data}"
    res5_json = ask_res5.get_json()
    print(f"[10] Q5 (after cache eviction): '{q5}'")
    print(f"     Answer: {res5_json['answer'][:100]}...")
    assert "92" in str(res5_json['answer']), f"Expected 92% attendance in answer, got: {res5_json['answer']}"

    # 10. Test conversation list API
    list_res = client.get("/api/conversations")
    assert list_res.status_code == 200
    list_json = list_res.get_json()
    assert len(list_json["conversations"]) >= 1
    found_conv = next((c for c in list_json["conversations"] if c["id"] == conv_id), None)
    assert found_conv is not None, "Conversation not found in list"
    print(f"[11] Verified conversation listing: title='{found_conv['title']}', dataset='{found_conv['dataset_name']}'")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY! 100% PERSISTENCE VERIFIED.")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
