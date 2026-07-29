"""card_schema.py - 카드/digest 필수 필드의 단일 정의.

scripts/lint_card.py, tools/build_index.py, tools/sync_db.py가 공유한다.
값을 여기서만 바꾸면 세 스크립트가 함께 갱신된다 (전에는 세 곳에 각각 다른
필수 필드 목록이 있어 lint는 통과 못 해도 index/DB 동기화는 통과하는 카드가
나올 수 있었다).

TYPE_VOCAB은 db/00_init_all.sql의 `type_vocab` CHECK 제약과 같은 값을
유지해야 한다 (SQL 쪽은 Python 상수를 직접 참조할 수 없어 수동 동기화 필요).
"""

CARD_REQUIRED = ["card_id", "type", "title", "summary", "tags", "updated", "confidence"]
DIGEST_REQUIRED = ["type", "period", "sources", "status"]

TYPE_VOCAB = {
    "ELEM":  {"mechanic", "narrative-device", "tone", "tech"},
    "GAME":  {"success", "failure", "mixed"},
    "GENRE": {"genre"},
    "ARCH":  {"pattern", "structure", "convention"},
}
