@echo off
REM UTF-8 인코딩 설정 (한글 깨짐 방지)
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo     논문 인용 관리 앱 실행기
echo ========================================

REM 작업 디렉토리 변경 및 확인
cd /d "C:\devData\work_2026\doc_annotation" || (
    echo [오류] 작업 디렉토리로 이동 실패!
    echo 경로: C:\devData\work_2026\doc_annotation
    pause
    exit /b 1
)
echo [확인] 작업 디렉토리: %CD%

REM 1단계: 가상환경 확인 및 생성
echo.
echo [1/5] 가상환경 확인/생성 중...
if not exist venv (
    echo    가상환경 생성...
    python -m venv venv
    if !errorlevel! neq 0 (
        echo [오류] 가상환경 생성 실패!
        pause
        exit /b 1
    )
    echo    가상환경 생성 완료 ✓
) else (
    echo    가상환경 이미 존재 ✓
)

REM 2단계: 가상환경 활성화
echo [2/5] 가상환경 활성화 중...
call venv\Scripts\activate.bat
if !errorlevel! neq 0 (
    echo [오류] 가상환경 활성화 실패!
    pause
    exit /b 1
)
echo    가상환경 활성화 완료 ✓

REM 3단계: Flask 설치 확인
echo [3/5] Flask 설치 확인 중...
pip install flask --quiet --upgrade
if !errorlevel! neq 0 (
    echo [경고] Flask 설치 중 오류 (계속 진행)
) else (
    echo    Flask 최신 버전 설치 완료 ✓
)

REM 4단계: 데이터베이스 초기화
echo [4/5] 데이터베이스 초기화 중...
python -c "from models import init_db; init_db()" 2>nul
if !errorlevel! neq 0 (
    echo [경고] DB 초기화 생략 (앱 실행시 자동 생성)
) else (
    echo    데이터베이스 초기화 완료 ✓
)

REM 5단계: 앱 실행
echo.
echo ========================================
echo 🎉 모든 준비 완료! 앱 실행 중...
echo ========================================
echo    🌐 접속 주소: http://127.0.0.1:5000
echo    💾 DB 위치: %CD%\data\annotation.db
echo    🎨 HTML 위치: %CD%\html
echo ========================================
echo.
echo 💡 사용법:
echo    - 논문 목록: http://127.0.0.1:5000
echo    - 새 논문: "논문추가" 버튼 클릭
echo    - 종료: Ctrl+C 후 창 닫기
echo ========================================

:run_app
echo.
echo [실행] Flask 서버 시작...
python app.py
if !errorlevel! neq 0 (
    echo.
    echo [오류] 앱 실행 실패. 3초 후 재시작...
    timeout /t 3 >nul
    goto run_app
)

echo.
echo [종료] 앱이 종료되었습니다.
pause
