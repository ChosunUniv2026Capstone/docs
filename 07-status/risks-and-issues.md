---
title: 리스크와 이슈
type: status
status: active
updated: 2026-03-30
owners:
  - team
related:
  - network-topology
  - req-device-auth
  - adr-0005-presence-snapshot-cache
source:
  - 06-meetings/raw/2026-03-19-capstone-proposal.md
  - 06-meetings/raw/2026-03-30-presence-logic-clarification.md
---

# 2026-03-30

- OpenWrt 또는 게이트웨이 환경에서 필요한 수준의 단말 정보를 안정적으로 수집할 수 있을지 검증이 필요하다.
- 단말 식별 정보 저장은 개인정보 및 보안 정책 검토가 필요하다.
- 랜덤 MAC 을 학생이 끄지 않으면 등록 단말 매칭이 실패할 수 있다.
- 문서보다 구현이 앞서가면 서비스 경계가 쉽게 섞일 수 있다.
- 시험 접근 제어 범위를 성급히 넓히면 운영 복잡도가 급격히 증가할 수 있다.
- Redis snapshot 캐시 만료 시 동시 요청이 몰리면 OpenWrt 수집 부하가 커질 수 있다.
