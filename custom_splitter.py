from langchain_core.documents import Document

def split_by_faq(docs: list[Document]):
    chunks = []
    for doc in docs:
        page_content = doc.page_content
        loops = 0
        while len(page_content) > 0:
            end = page_content.find('\n\n')
            if end < 0:
                chunk = Document(page_content=page_content)
                chunks.append(chunk)
                break
            chunk = Document(page_content=page_content[:end], metadata=doc.metadata)
            chunks.append(chunk)
            page_content = page_content[end+2:]
            loops += 1
    print(loops)
    return chunks