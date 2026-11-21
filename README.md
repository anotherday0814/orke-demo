# orke-demo

JAX·PyTorch 설치 확인 스크립트, 브라우저용 할 일 목록 페이지, Claude API로 코드 변경을 리뷰하는 스크립트를 모아 둔 작은 예제 모음입니다.

## 파일 구성

| 파일 | 용도 |
|---|---|
| `todo.html` | 브라우저에서 바로 여는 할 일 목록 페이지 (서버·설치 불필요) |
| `jax_test.py` | JAX 설치 확인: `grad`, `jit` 동작 점검 |
| `torch_test.py` | PyTorch 설치 확인: autograd와 간단한 선형 회귀 학습 |
| `review_diff.py` | 코드 변경(diff)을 Claude API로 보내 보안·성능 리뷰 받기 |
| `requirements-jax.txt` | `jax_test.py`용 패키지 버전 |
| `requirements-torch.txt` | `torch_test.py`용 패키지 버전 |

## todo.html

할 일을 추가하고, 완료 표시하고, 삭제할 수 있는 한 페이지짜리 앱입니다. 목록은 브라우저의 `localStorage`에 저장되므로 새로고침해도 남아 있고, 외부로 전송되지 않습니다. 시스템 설정에 따라 다크 모드도 지원합니다.

**실행:** 파일을 더블클릭하거나 브라우저 창으로 끌어다 놓으면 됩니다.

## jax_test.py

JAX가 제대로 설치됐는지 확인합니다.

- JAX 버전, 기본 백엔드, 사용 가능한 장치 출력
- `jax.grad`로 f(x) = x³ + 2x 의 x=2 에서의 미분값 계산 (기대값 14.0)
- `jax.jit`으로 컴파일한 SELU 함수 실행
- `jax.jit(jax.grad(f))`로 x=3 에서의 미분값 계산 (기대값 29.0)

**실행 (Windows PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-jax.txt
.\.venv\Scripts\python.exe jax_test.py
```

macOS/Linux에서는 `.venv/bin/python`을 사용하세요.

## torch_test.py

PyTorch가 제대로 설치됐는지 확인합니다.

- PyTorch 버전, CUDA 사용 가능 여부, 사용 장치, CPU 스레드 수 출력
- autograd로 y = x³ + 2x 의 x=2 에서의 미분값 계산 (기대값 14.0)
- 잡음이 섞인 y = 3x + 1 데이터로 선형 회귀를 1000 epoch 학습하고 학습된 기울기·절편 출력

**실행:**

```powershell
pip install -r requirements-torch.txt
python torch_test.py
```

GPU가 없어도 CPU로 동작합니다. CUDA 빌드가 필요하면 [PyTorch 설치 안내](https://pytorch.org/get-started/locally/)를 참고하세요.

## review_diff.py

코드 변경(diff)을 Claude API에 보내 보안 위험(인젝션, 인증 누락, 비밀값 노출 등)과 성능 문제(N+1 쿼리, 불필요한 I/O 등)를 심각도 순으로 리뷰받습니다. 결과는 스트리밍으로 출력됩니다.

**준비:**

```powershell
pip install anthropic
$env:ANTHROPIC_API_KEY = "본인의 API 키"   # macOS/Linux: export ANTHROPIC_API_KEY=...
```

API 키는 코드나 저장소에 넣지 말고 환경 변수로만 설정하세요.

**실행:**

```powershell
python review_diff.py                         # 현재 git 저장소의 `git diff HEAD` 리뷰
python review_diff.py change.diff             # 파일에 저장된 diff 리뷰
git diff main... | python review_diff.py -    # 표준 입력으로 받은 diff 리뷰
python review_diff.py --model <모델 ID>        # 다른 모델 사용
```

기본 모델은 `claude-sonnet-5-5`이며, 30만 자가 넘는 diff는 앞부분만 리뷰합니다.
