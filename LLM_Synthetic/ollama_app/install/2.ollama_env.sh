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

    case "$OS" in
        rhel|centos|rocky|almalinux|fedora)
            if command -v getenforce >/dev/null 2>&1; then

                SELINUX_STATUS=$(getenforce)

                echo "SELinux 상태: $SELINUX_STATUS"

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
            ;;
    esac

}

log "=== Ollama  환경 설정  시작 ==="

#################################################################3

# 환경 변수 설정 파일 생성
log "환경 변수 설정 파일 생성"
cat > "${INSTALL_DIR}/ollama_env.sh" << 'EOF'
#!/bin/bash
export OLLAMA_HOME=/data/ollama_app
export OLLAMA_MODELS=/data/ollama_app/models
export OLLAMA_HOST=0.0.0.0:11434
export PATH=/data/ollama_app:$PATH
echo "Ollama 환경 변수 로드 완료"
EOF

chmod +x "${INSTALL_DIR}/ollama_env.sh"

# 시작/정지 스크립트 생성
log "관리 스크립트 생성"

cat > "${INSTALL_DIR}/start_ollama.sh" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/logs/ollama.log"
source "${SCRIPT_DIR}/ollama_env.sh"

if pgrep -f "ollama serve" > /dev/null; then
    echo "Ollama가 이미 실행 중입니다."
    exit 1
fi

echo "Ollama 시작 중..."
nohup "${SCRIPT_DIR}/ollama" serve >> "$LOG_FILE" 2>&1 &
sleep 3

if pgrep -f "ollama serve" > /dev/null; then
    echo "✓ Ollama 시작 완료 (포트: 11434)"
else
    echo "✗ 시작 실패. 로그: $LOG_FILE"
    exit 1
fi
EOF

cat > "${INSTALL_DIR}/stop_ollama.sh" << 'EOF'
#!/bin/bash
if pgrep -f "ollama serve" > /dev/null; then
    pkill -f "ollama serve"
    sleep 2
    if pgrep -f "ollama serve" > /dev/null; then
        pkill -9 -f "ollama serve"
    fi
    echo "✓ Ollama 정지 완료"
else
    echo "실행 중인 Ollama 없음"
fi
EOF

cat > "${INSTALL_DIR}/status_ollama.sh" << 'EOF'
#!/bin/bash
if pgrep -f "ollama serve" > /dev/null; then
    echo "✓ Ollama 실행 중"
    ps aux | grep "ollama serve" | grep -v grep
else
    echo "✗ Ollama 정지됨"
fi
EOF

chmod +x "${INSTALL_DIR}"/*.sh

# SELinux 설정 (Red Hat 계열)
configure_selinux

# systemd 서비스 생성
log "systemd 서비스 설정"
read -p "systemd 서비스로 등록하시겠습니까? [Y/n]: " create_service
create_service=${create_service:-Y}

if [[ "$create_service" =~ ^[Yy]$ ]]; then
    sudo tee /etc/systemd/system/ollama.service > /dev/null << EOF
[Unit]
Description=Ollama Service
Documentation=https://ollama.ai/
After=network-online.target
Wants=network-online.target

[Service]
Type=exec
User=$USER
Group=$USER
ExecStart=${INSTALL_DIR}/ollama serve
Environment="OLLAMA_HOME=${INSTALL_DIR}"
Environment="OLLAMA_MODELS=${MODELS_DIR}"
Environment="OLLAMA_HOST=0.0.0.0:11434"
Restart=always
RestartSec=3
StandardOutput=append:${INSTALL_DIR}/logs/ollama.log
StandardError=append:${INSTALL_DIR}/logs/ollama_error.log
LimitNOFILE=65536
LimitNPROC=4096

[Install]
WantedBy=default.target
EOF

    sudo systemctl daemon-reload
    sudo systemctl enable ollama
    log "Ollama 서비스 시작 중..."
    sudo systemctl start ollama
    sleep 3
    
    if sudo systemctl is-active --quiet ollama; then
        log "✓ Ollama 서비스 시작 완료"
    else
        error "✗ 서비스 시작 실패"
        sudo systemctl status ollama --no-pager
    fi
fi

# 방화벽 설정
configure_firewall

# 환경 변수를 shell rc 파일에 추가
log "환경 변수 설정"

# bash 사용자
if [ -f ~/.bashrc ]; then
    if ! grep -q "OLLAMA_HOME=${INSTALL_DIR}" ~/.bashrc; then
        cat >> ~/.bashrc << EOF

# Ollama 환경 변수
export OLLAMA_HOME=${INSTALL_DIR}
export OLLAMA_MODELS=${MODELS_DIR}
export PATH=${INSTALL_DIR}:\$PATH
EOF
        log "~/.bashrc에 환경 변수 추가됨"
    fi
fi

# zsh 사용자
if [ -f ~/.zshrc ]; then
    if ! grep -q "OLLAMA_HOME=${INSTALL_DIR}" ~/.zshrc; then
        cat >> ~/.zshrc << EOF

# Ollama 환경 변수
export OLLAMA_HOME=${INSTALL_DIR}
export OLLAMA_MODELS=${MODELS_DIR}
export PATH=${INSTALL_DIR}:\$PATH
EOF
        log "~/.zshrc에 환경 변수 추가됨"
    fi
fi

. ${INSTALL_DIR}/ollama_env.sh
source ${INSTALL_DIR}/ollama_env.sh

log "=== 설치 완료! ==="

cat << EOF

╔═══════════════════════════════════════════════════════════╗
║          Ollama 설치 완료 ($OS_NAME)                      
╚═══════════════════════════════════════════════════════════╝

📁 설치 경로: ${INSTALL_DIR}
📦 모델 경로: ${MODELS_DIR}
📋 로그 파일: ${INSTALL_DIR}/logs/

🚀 서비스 관리:
   sudo systemctl start ollama
   sudo systemctl stop ollama
   sudo systemctl restart ollama
   sudo systemctl status ollama
   sudo journalctl -u ollama -f

📚 모델 관리:
   ollama pull deepseek-coder:6.7b
   ollama list
   ollama run deepseek-coder

⚙️  환경 변수: source ${INSTALL_DIR}/ollama_env.sh

EOF

exit 0
