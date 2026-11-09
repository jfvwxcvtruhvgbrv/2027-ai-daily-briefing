# 이슈 JSON 스키마 (`issues/YYYY-MM-DD.json`)

매일 아침 Claude 예약 작업이 이 형식으로 파일 1개를 만들어 push합니다.
GitHub Actions(`render/build.py`)가 이 파일을 읽어 보고서(Pages)를 만듭니다.
필수 항목이 빠지면 빌드가 실패합니다(조용한 실패 방지, 이전 사이트는 유지).

## 최상위

| 키 | 필수 | 설명 |
|---|---|---|
| `date` | ✅ | `YYYY-MM-DD` (KST 발행일, 파일명과 같아야 함) |
| `weekday` | ✅ | `월`~`일` |
| `period` | ✅ | 대상 기간 표기, 예 `11/8 ~ 11/9` |
| `tagline` | ✅ | 오늘의 핵심 한 줄 (지난 호 목록에 표시) |
| `key_points` | ✅ | 핵심 3줄 (문자열 3개) |
| `top_story` | ✅ | 1면 톱 기사 (article) |
| `sketchlab` | ✅ | SketchLab 심층 리포트 목록 (sketchlab_item, 새 항목 없으면 빈 배열) |
| `sections` | ✅ | `[{ "name": "모델·제품 출시", "articles": [article, ...] }, ...]` |
| `korea` | ✅ | 한국 AI 기사 목록 (article) |
| `briefs` | ✅ | 단신 `[{ "text", "grade", "sources": [source] }]` |
| `social` | ✅ | X·LinkedIn `[{ "who", "text", "date", "grade", "url" }]`. 확인된 포스트가 없으면 빈 배열 |
| `editorial` | ✅ | 해설 `{ "title", "body" }` |
| `calendar` | ✅ | 일정 `[{ "when", "what", "grade" }]` (`grade` 생략 가능) |
| `coverage` | ✅ | 이번 호 취재 범위 한 줄 |
| `sketchlab_last` | ✅ | 이번에 처리한 SketchLab 최대 번호(새 항목 없으면 이전 값) |
| `notes` | | 편집 한계·미확인 사항 메모 (문자열 배열) |

## article

| 키 | 필수 | 설명 |
|---|---|---|
| `category` | ✅ | 예 `빅테크`, `투자`, `에이전트` |
| `grade` | ✅ | `primary`(✅ 1차 출처) / `multi`(☑️ 복수 매체) / `single`(⚠️ 단일 출처·협상 중) |
| `headline` | ✅ | 헤드라인 |
| `lead` | ✅ | 리드 1~2문장 |
| `body` | | 본문 단락 배열 (1면 톱·한국 톱은 3~4단락) |
| `why` | ✅ | 💡 왜 중요한가 1~2문장 |
| `image_page` | | 대표 이미지를 가져올 **기업 공식 페이지** URL(공식 블로그·뉴스룸·제품 발표). Actions가 og:image를 찾아 붙임. 인물·보도사진이 대표 이미지인 페이지는 넣지 말 것 |
| `image_caption` | | 이미지 설명 (출처 표기는 자동) |
| `chart` | | `{ "title", "unit", "source", "bars": [{ "label", "value", "highlight": true/false }] }` 공개 수치만 |
| `sources` | ✅ | `[{ "name", "url", "date" }]` 1개 이상, 원문·공식 출처 우선 |

## sketchlab_item = article + 아래 키

| 키 | 필수 | 설명 |
|---|---|---|
| `no` | ✅ | SketchLab 번호 (정수) |
| `tags` | ✅ | SketchLab 태그 문자열 |
| `what` / `numbers` / `competition` / `reaction` / `availability` | | 심층 소제목별 단락 (무엇인가 / 핵심 수치 / 경쟁 구도 / X·업계 반응 / 써볼 수 있나) |

## 원칙
- 원문 문장 복사 금지, 직접 재작성. 인용은 15단어 미만 1회
- 수치는 원문에서 확인, 매체별로 다르면 범위로 표기
- X·LinkedIn 포스트는 실제로 확인된 것만. 지어내지 않음
- 투자 판단 근거 아님 (고지는 자동 삽입)
