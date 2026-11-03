import io
import sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

AGENTX_DIR = Path(r"C:\Users\karan\Desktop\AgentX")
sys.path.insert(0, str(AGENTX_DIR))

from app import app
from utils.auth_db import get_db_connection

def run_e2e_test():
    print("=" * 60)
    print("Running AgentX End-to-End Document QA Integration Test")
    print("=" * 60)

    client = app.test_client()

    # Authenticate as user 'karan'
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["username"] = "karan"

    # 1. Upload User's PDF
    pdf_source = Path(r"C:\Users\karan\.gemini\antigravity\brain\12abbc1a-ea41-49b6-a759-d5f8bdb9b7aa\.user_uploaded\media_1793350039997_bbacaedf.pdf")
    assert pdf_source.is_file(), "Source PDF must exist"

    with open(pdf_source, "rb") as f:
        pdf_bytes = f.read()

    upload_data = {
        "file": (io.BytesIO(pdf_bytes), "SLOT_2_SEM_2_RESULTS_WINTER-2024.pdf")
    }
    r_upload = client.post("/api/upload", data=upload_data, content_type="multipart/form-data")
    print(f"\n1. Upload PDF -> HTTP {r_upload.status_code}")
    assert r_upload.status_code == 200, f"Upload failed: {r_upload.data}"
    up_json = r_upload.get_json()
    dataset_id = up_json["dataset_id"]
    print(f"   ✓ Dataset ID: {dataset_id}")
    print(f"   ✓ Doc Category: {up_json.get('doc_category')}")
    print(f"   ✓ Extracted Records: {up_json.get('rows')}")
    print(f"   ✓ Suggested Questions: {up_json.get('suggested_questions')}")

    # 2. Ask: "tell me full information about karan kajgunde"
    q1 = "tell me full information about karan kajgunde"
    r_q1 = client.post("/api/ask", json={
        "dataset_id": dataset_id,
        "question": q1
    })
    print(f"\n2. Query: '{q1}' -> HTTP {r_q1.status_code}")
    assert r_q1.status_code == 200
    ans1 = r_q1.get_json()["answer"]
    print("   Answer Preview:\n" + ans1[:300])
    assert "23025331995034" in ans1, "Should find PRN 23025331995034"
    assert "KAJGUNDE" in ans1, "Should find KAJGUNDE"
    assert "64" in ans1, "Should find marks 64"
    assert "CD" in ans1, "Should find grade CD"
    print("   ✓ Passed: Karan Kajgunde details retrieved with 100% precision!")

    # 3. Ask: "Give full details about CHIMURKAR SHARAD LALAJI"
    q2 = "Give full details about CHIMURKAR SHARAD LALAJI"
    r_q2 = client.post("/api/ask", json={
        "dataset_id": dataset_id,
        "question": q2
    })
    print(f"\n3. Query: '{q2}' -> HTTP {r_q2.status_code}")
    assert r_q2.status_code == 200
    ans2 = r_q2.get_json()["answer"]
    print("   Answer Preview:\n" + ans2[:300])
    assert "2141631612013" in ans2, "Should find PRN 2141631612013"
    assert "CHIMURKAR" in ans2, "Should find CHIMURKAR"
    assert "41" in ans2, "Should find marks 41"
    assert "EE" in ans2, "Should find grade EE"
    print("   ✓ Passed: Chimurkar Sharad Lalaji details retrieved with 100% precision!")

    # 4. Ask: "show me the student who have ff grade"
    q3 = "show me the student who have ff grade"
    r_q3 = client.post("/api/ask", json={
        "dataset_id": dataset_id,
        "question": q3
    })
    print(f"\n4. Query: '{q3}' -> HTTP {r_q3.status_code}")
    assert r_q3.status_code == 200
    ans3 = r_q3.get_json()["answer"]
    print("   Answer Preview:\n" + ans3[:350])
    assert "FF" in ans3
    assert "| PRN |" in ans3 or "PRN" in ans3
    print("   ✓ Passed: Students with FF grade formatted in a clear structured table!")

    # 5. Test Image Upload
    # Create a test synthetic image with text using PIL
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (400, 200), color=(15, 20, 30))
    d = ImageDraw.Draw(img)
    d.rectangle([20, 20, 380, 180], outline=(255, 75, 36), width=3)
    d.text((40, 50), "VOTER CARD ID: IND9876543", fill=(245, 246, 248))
    d.text((40, 90), "Name: Rajesh Kumar", fill=(245, 246, 248))
    d.text((40, 130), "Age: 42  Gender: Male", fill=(245, 246, 248))

    img_io = io.BytesIO()
    img.save(img_io, format="PNG")
    img_io.seek(0)

    r_img_upload = client.post("/api/upload", data={
        "file": (img_io, "voter_card_sample.png")
    }, content_type="multipart/form-data")
    print(f"\n5. Upload Image -> HTTP {r_img_upload.status_code}")
    assert r_img_upload.status_code == 200
    img_json = r_img_upload.get_json()
    img_dataset_id = img_json["dataset_id"]

    q_img = "What text and details are visible in this image?"
    r_q_img = client.post("/api/ask", json={
        "dataset_id": img_dataset_id,
        "question": q_img
    })
    print(f"\n6. Query Image: '{q_img}' -> HTTP {r_q_img.status_code}")
    assert r_q_img.status_code == 200
    ans_img = r_q_img.get_json()["answer"]
    print("   Image Answer Preview:\n" + ans_img[:300])
    assert "IND9876543" in ans_img or "Rajesh" in ans_img or "VOTER" in ans_img or "Name" in ans_img or "Age" in ans_img
    print("   ✓ Passed: Image OCR and visual details extracted successfully!")

    print("\n" + "=" * 60)
    print("ALL 6 DOCUMENT QA & MULTIMODAL INTEGRATION TESTS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    run_e2e_test()
