
def answer():
    import os

    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    doc_path = os.path.join(desktop_path, "Стих.docx")
    
    if os.path.exists(doc_path):
        os.remove(doc_path)
        return "Я удалила документ Word на рабочем столе."
    else:
        return "Документ 'Стих.docx' не найден на рабочем столе."

