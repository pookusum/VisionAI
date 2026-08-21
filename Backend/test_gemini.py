from services.gemini_service import analyze_image


IMAGE_PATH = "test.jpg"


with open(IMAGE_PATH, "rb") as image_file:
    image_bytes = image_file.read()


result = analyze_image(
    image_bytes=image_bytes,
    mime_type="image/jpeg"
)


print("\n===== STRUCTURED GEMINI RESULT =====\n")

print("Caption:")
print(result["caption"])

print("\nDescription:")
print(result["description"])

print("\nScene:")
print(result["scene"])

print("\nObjects:")

for obj in result["objects"]:
    print(f"- {obj['name']}: {obj['description']}")

print("\nActivities:")

for activity in result["activities"]:
    print(f"- {activity}")