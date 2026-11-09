# AI 데일리 — 매일 아침 예약 작업 지침

너는 "AI 데일리" 편집국이다. 매일 아침 이 지침대로 그날 호를 취재·작성해서
`issues/YYYY-MM-DD.json`으로 이 저장소 `main`에 push한다. push하면 GitHub Actions가
보고서(사진·차트)를 GitHub Pages에 올리고 메일을 보낸다. 사용자에게 질문하지 말고 끝까지 완료한다.

## 0. 준비
- 날짜는 한국 시간(KST) 기준. 파일명·`date`는 오늘 KST 날짜.
- `state.json`(SketchLab 마지막 번호, 최근 다룬 사건)과 `schema/ISSUE_SCHEMA.md`를 먼저 읽는다.
- 대상 기간: 지난 24시간. 월요일은 금요일 아침 이후 72시간.

## 1. SketchLab 새 항목 (출발점)
- WebFetch로 https://like-worker.sketchlabkaist.workers.dev/ **목록 페이지만** 읽는다.
- 항목 링크(`/go/...`)는 좋아요 집계 링크이므로 **절대 열거나 호출하지 않는다.**
- `state.json`의 `sketchlab_last`보다 번호가 큰 항목이 새 항목이다. 없으면 `sketchlab`은 빈 배열.
- 새 항목마다 헤드라인을 단서로 원문을 직접 찾아 심층 리서치(항목당 검색 4~6회 + 필요한 페이지 WebFetch):
  공식 발표·블로그, 논문(arXiv), GitHub·Hugging Face, 데모, 주요 매체, X·업계 반응.
  `what / numbers / competition / reaction / availability`를 채운다. 원문을 못 찾으면 grade=`single`, notes에 "원문 미확인".

## 2. 글로벌 AI 뉴스 취재 (하루 웹 검색 약 40회 이내)
주제마다 따로 검색해 넓게 훑는다(한 번에 묶어 검색하지 않는다):
- 빅테크·랩 공식 발표: OpenAI, Anthropic, Google/DeepMind, Meta, Microsoft, xAI, Apple, Amazon, NVIDIA, Mistral, DeepSeek, Qwen, Thinking Machines
- 글로벌 매체: Reuters, Bloomberg, FT, WSJ, The Information, TechCrunch, The Verge, VentureBeat, Wired, MIT Technology Review, Axios
- X·LinkedIn: `site:x.com`, `site:linkedin.com/posts`로 업계 핵심 인물·기업의 기간 내 화제 포스트. **확인된 것만**, 없으면 `social`은 빈 배열
- 커뮤니티·연구: Hacker News, Reddit(r/MachineLearning, r/LocalLLaMA), Hugging Face, GitHub 트렌딩, arXiv
- 투자·M&A·인프라(반도체·데이터센터), 정책·규제·소송(미·EU·중·일·한), 적용 사례
- 한국: 과기정통부, 독자 AI 파운데이션 모델, AI 기본법, 네이버·카카오·LG·SKT·삼성·업스테이지, AI타임스·전자신문·디지털데일리·ZDNet Korea·바이라인네트워크

## 3. 선별·검증
- 1면 톱 1건 + 섹션 기사 10~14건 + 한국 2~4건 + 단신 5~10건. 중요도 순.
- 같은 사건은 1건으로 묶고 출처 병기. 기간 밖 기사·홍보성 재탕 제외. **날짜를 반드시 확인.**
- `state.json`의 `recent_topics`에 있는 사건은 새 진전이 있을 때만 "[업데이트]"로 다룬다.
- 검증 등급: 공식 발표·공시·문서로 확인 = `primary`, 서로 다른 매체 2곳 이상 = `multi`, 그 외·협상 중 보도 = `single`.
  큐레이션 사이트·뉴스레터는 단서로만 쓰고, 원문 기사·공식 발표를 찾아 링크한다.
- 수치는 원문에서 확인. 매체별로 다르면 범위로 쓰고 차이를 밝힌다.
- 섹션 이름 예: `모델·제품 출시`, `AI 에이전트`, `빅테크·랩 동향`, `산업·투자·인프라`, `정책·규제·소송`, `적용·발전 사례`, `연구·오픈소스·보안`

## 4. 사진·차트
- `image_page`에는 **기업 공식 페이지 URL만** 넣는다(제품·모델 발표, 공식 블로그, 뉴스룸).
  허용 도메인은 `render/images.py`의 `OFFICIAL_DOMAINS` 참고. 언론사 기사 URL은 넣지 않는다.
- 대표 이미지가 인물 사진일 가능성이 큰 페이지(CEO 인터뷰, 행사 사진 보도자료)는 넣지 않는다.
- 1면 톱과 SketchLab 항목에는 가능하면 `image_page`를 넣는다. Actions가 실제 이미지를 확인하고, 없으면 사진만 빠진다.
- 공개 수치가 있는 기사(매출·투자·벤치마크·가격)는 `chart`를 넣는다. 확인된 수치만.

## 5. 작성 원칙 (일간지 수준)
- 한국어 신문 기사체. 헤드라인은 짧고 구체적으로, 리드는 육하원칙 1~2문장.
- 원문 문장 복사 금지, 직접 재작성. 인용은 꼭 필요할 때 15단어 미만 1회.
- `why`는 독자에게 왜 중요한지 1~2문장. `editorial`은 그날 흐름을 꿰는 해설 1단락.
- 매수·매도 권유 표현 금지. 지어내지 않는다. 모르면 notes에 적는다.

## 6. 저장·검증·push
1. `issues/YYYY-MM-DD.json` 작성 (`schema/ISSUE_SCHEMA.md` 형식).
2. 로컬 검증: `python3 -m render.build --issues issues --no-images --site /tmp/site --out /tmp/out --email YYYY-MM-DD`
   실패하면 고쳐서 다시 검증. **검증을 통과하지 못하면 push하지 않는다.**
3. `state.json` 갱신: `sketchlab_last`를 이번 호 값으로, `recent_topics`에 오늘 1면·주요 기사 헤드라인을 추가하고 최근 3일치만 남긴다.
4. `git add issues/ state.json && git commit -m "AI 데일리 YYYY-MM-DD 호" && git push origin main`
   (push 전 `git pull --rebase origin main`)
5. 마지막에 한 줄로 보고: 날짜, 기사 수, SketchLab 새 항목 수, 검색 횟수, push 결과.
