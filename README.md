# AI 데일리 — 매일 아침 글로벌 AI 일간 브리핑

매일 아침 7시 전후(KST) 전세계 AI 생태계 소식을 일간지 형식으로 정리해
**웹 보고서(GitHub Pages, 사진·차트·심층 리포트)** 로 발행한다. 메일은 보내지 않는다.

- 최신 호(북마크용): `https://jfvwxcvtruhvgbrv.github.io/2027-ai-daily-briefing/latest.html`
- 지난 호 모아보기: `https://jfvwxcvtruhvgbrv.github.io/2027-ai-daily-briefing/`

## 동작 방식
```
[Claude 예약 작업 — Claude Pro 구독 사용량, API 비용 없음]
  주요소스 새 항목 → 원문 추적 심층 리서치
  + 글로벌·국내 AI 뉴스 취재 → 교차 검증(✅ ☑️ ⚠️) → 기사·1면·해설 작성
  → issues/YYYY-MM-DD.json push   (지침: prompts/daily_task.md)
        ↓ push 트리거
[GitHub Actions — 무료]  .github/workflows/publish.yml
  공식 페이지 대표 이미지 확인 → 일간지형 보고서 → GitHub Pages
```

| 경로 | 역할 |
|---|---|
| `issues/` | 날짜별 호 (JSON) |
| `schema/ISSUE_SCHEMA.md` | 호 JSON 형식 |
| `prompts/daily_task.md` | 매일 예약 작업이 따르는 취재·편집 지침 |
| `key_sources.json` | 주요소스 목록 (사용자가 수시로 추가) |
| `state.json` | 주요소스별 마지막 확인 위치, 최근 다룬 사건 |
| `render/` | 검증·이미지 확인·보고서 템플릿·빌드 |
| `examples/` | 렌더링 테스트용 샘플 |

## 처음 한 번 설정
1. **Claude GitHub 앱 권한**: https://github.com/apps/claude/installations/select_target 에서 이 저장소 추가 (예약 작업이 push하려면 필요)
2. **GitHub Pages**: Settings → Pages → Build and deployment → Source를 **GitHub Actions**로
(Secrets 등록 불필요)

## 수동 실행
- Actions → "AI 데일리 발행 (Pages)" → Run workflow: 사이트 전체 재빌드·재배포
- 로컬 확인: `python3 -m render.build --issues examples --no-images` → `site/`

## 실패하면
- 호 JSON 형식 오류 → Actions가 실패로 끝나고 GitHub 실패 알림 메일이 옴 (이전 사이트는 그대로 유지)
- 공식 이미지를 못 찾으면 사진만 빠지고 계속 진행 (로그에 `[WARN] 이미지`)
- 예약 작업이 실패하면 push가 없어 그날 호가 올라오지 않음 (예약 작업 실패 알림 확인)

## 원칙
- 원문 복사 금지, 직접 재작성 요약 + 원문 링크
- 사진은 기업 공식 페이지 대표 이미지만 원본 주소로 싣고 출처 표기, 인물·보도사진 제외, 저장소에 복사하지 않음
- 주요소스는 `key_sources.json`의 소스별 읽기 규칙(`how`)을 따름 (예: 목록 페이지만 읽고 집계 링크는 호출하지 않음)
- X·LinkedIn은 공개 웹 검색으로 확인된 포스트만
- 투자 판단의 근거가 아님
