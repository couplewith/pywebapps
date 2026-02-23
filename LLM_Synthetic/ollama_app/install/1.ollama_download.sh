#!/bin/bash

#############################################
# Ollama 통합 설치 스크립트
# 지원 OS: Ubuntu 22.04, RHEL/CentOS 7/8/9
# 설치 경로: /data/ollama_app
#############################################

set -e

# 설정 변수
INSTALL_DIR="/data/ollama_app"
MODELS_DIR="${INSTALL_DIR}/models"
OLLAMA_URL="https://github.com/ollama/ollama/releases/download/v0.13.5/ollama-linux-arm64.tgz"
OLLAMA_FILE=$(basename ${OLLAMA_URL})
LOG_FILE="${INSTALL_DIR}/install.log"

# 색상 코드
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

# OS 감지 함수
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
        OS_VERSION=$VERSION_ID
        OS_NAME=$NAME
    elif [ -f /etc/redhat-release ]; then
        OS="rhel"
        OS_VERSION=$(cat /etc/redhat-release | grep -oP '[0-9]+' | head -1)
        OS_NAME=$(cat /etc/redhat-release)
    else
        error "지원하지 않는 운영체제입니다."
        exit 1
    fi
    
    log "감지된 OS: $OS_NAME (버전: $OS_VERSION)"
    
    case $OS in
        ubuntu|debian)
            PKG_MANAGER="apt"
            INSTALL_CMD="apt install -y"
            UPDATE_CMD="apt update"
            ;;
        rhel|centos|rocky|almalinux|fedora)
            if command -v dnf &> /dev/null; then
                PKG_MANAGER="dnf"
                INSTALL_CMD="dnf install -y"
                UPDATE_CMD="dnf check-update || true"
            else
                PKG_MANAGER="yum"
                INSTALL_CMD="yum install -y"
                UPDATE_CMD="yum check-update || true"
            fi
            ;;
        *)
            error "지원하지 않는 OS: $OS"
            exit 1
            ;;
    esac
    
    log "패키지 관리자: $PKG_MANAGER"
}

# 필수 패키지 설치
install_dependencies() {
    log "필수 패키지 설치 중..."
    
    sudo $UPDATE_CMD
    
    case $OS in
        ubuntu|debian)
            sudo $INSTALL_CMD curl wget ca-certificates gnupg lsb-release
            ;;
        rhel|centos|rocky|almalinux|fedora)
            sudo $INSTALL_CMD curl wget ca-certificates
            ;;
    esac
}

# 방화벽 설정
configure_firewall() {
    log "방화벽 설정 확인 중..."
    
    case $OS in
        ubuntu|debian)
            if command -v ufw &> /dev/null; then
                if sudo ufw status | grep -q "Status: active"; then
                    warning "UFW 방화벽이 활성화되어 있습니다."
                    read -p "포트 11434를 열겠습니까? [y/N]: " open_port
                    if [[ "$open_port" =~ ^[Yy]$ ]]; then
                        sudo ufw allow 11434/tcp
                        log "UFW: 포트 11434가 열렸습니다."
                    fi
                fi
            fi
            ;;
        rhel|centos|rocky|almalinux|fedora)
            if command -v firewall-cmd &> /dev/null; then
                if sudo firewall-cmd --state 2>/dev/null | grep -q "running"; then
                    warning "firewalld가 활성화되어 있습니다."
                    read -p "포트 11434를 열겠습니까? [y/N]: " open_port
                    if [[ "$open_port" =~ ^[Yy]$ ]]; then
                        sudo firewall-cmd --permanent --add-port=11434/tcp
                        sudo firewall-cmd --reload
                        log "firewalld: 포트 11434가 열렸습니다."
                    fi
                fi
            fi
            ;;
    esac
}

# SELinux 설정 (Red Hat 계열)
configure_selinux() {
    if [[ "$OS" =~ ^(rhel|centos|rocky|almalinux|fedora)$ ]]; then
        if command -v getenforce &> /dev/null; then
            SELINUX_STATUS=$(getenforce)
            log "SELinux 상태: $SELINUX_STATUS"
            
            if [ "$SELINUX_STATUS" != "Disabled" ]; then
                warning "SELinux가 활성화되어 있습니다."
                log "SELinux 컨텍스트 설정 중..."
                
                # 디렉토리에 대한 SELinux 컨텍스트 설정
                sudo semanage fcontext -a -t bin_t "${INSTALL_DIR}/ollama" 2>/dev/null || true
                sudo restorecon -v "${INSTALL_DIR}/ollama" 2>/dev/null || true
                
                # 포트 허용
                sudo semanage port -a -t http_port_t -p tcp 11434 2>/dev/null || \
                sudo semanage port -m -t http_port_t -p tcp 11434 2>/dev/null || true
                
                log "SELinux 설정 완료"
            fi
        fi
    fi
}

log "=== Ollama 통합 설치 시작 ==="

# OS 감지
detect_os

# Root 권한 확인
if [ "$EUID" -eq 0 ]; then
    error "이 스크립트를 root로 실행하지 마세요."
    exit 1
fi

# sudo 권한 확인
if ! sudo -v; then
    error "sudo 권한이 필요합니다."
    exit 1
fi

# 필수 패키지 설치
install_dependencies

# 설치 디렉토리 생성
log "설치 디렉토리 생성: ${INSTALL_DIR}"
if [ ! -d "$INSTALL_DIR" ]; then
    sudo mkdir -p "$INSTALL_DIR"
fi
sudo chown -R $USER:$USER "$INSTALL_DIR"
mkdir -p "$MODELS_DIR"
mkdir -p "${INSTALL_DIR}/logs"

# Ollama 바이너리 다운로드
log "Ollama 바이너리 다운로드 중..."
cd "$INSTALL_DIR"

if [ -f "ollama" ]; then
    log "기존 Ollama 백업 중..."
    mv ollama ollama.backup.$(date +%Y%m%d_%H%M%S)
fi

if ! wget -O ollama "$OLLAMA_URL" 2>&1 | tee -a "$LOG_FILE"; then
    if ! curl -L "$OLLAMA_URL" -o ollama 2>&1 | tee -a "$LOG_FILE"; then
        error "다운로드 실패"
        exit 1
    fi
fi
log "다운로드 완료 [$?] "

chmod +x ollama


