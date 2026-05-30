from pathlib import Path


def load_knowledge_base() -> str:
    data_folder = Path("data")

    if not data_folder.exists():
        return "База знаний не найдена."

    knowledge_parts = []

    for file_path in data_folder.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")

        knowledge_parts.append(
            f"\n--- FILE: {file_path.name} ---\n{content}"
        )

    if not knowledge_parts:
        return "В базе знаний пока нет информации."

    return "\n".join(knowledge_parts)