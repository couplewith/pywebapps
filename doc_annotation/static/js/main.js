// 논문 인용 관리 앱 JavaScript

// DOM 로드 완료 시 실행
document.addEventListener('DOMContentLoaded', function() {
    console.log('📚 논문 인용 관리 앱 로드 완료');
    
    // 삭제 확인 다이얼로그
    initDeleteConfirm();
    
    // 폼 유효성 검사
    initFormValidation();
    
    // 자동 저장 기능 (선택)
    // initAutoSave();
});

// 삭제 확인
function initDeleteConfirm() {
    const deleteLinks = document.querySelectorAll('a[href*="delete"]');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('정말 삭제하시겠습니까?')) {
                e.preventDefault();
            }
        });
    });
}

// 폼 유효성 검사
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#f56565';
                } else {
                    field.style.borderColor = '#e2e8f0';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('필수 입력 항목을 확인해주세요.');
            }
        });
    });
}

// 자동 저장 (로컬스토리지)
function initAutoSave() {
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        const saveKey = 'autosave_' + textarea.name;
        
        // 저장된 내용 복구
        const saved = localStorage.getItem(saveKey);
        if (saved && !textarea.value) {
            textarea.value = saved;
        }
        
        // 자동 저장
        textarea.addEventListener('input', function() {
            localStorage.setItem(saveKey, this.value);
        });
        
        // 폼 제출 시 자동 저장 삭제
        const form = textarea.closest('form');
        if (form) {
            form.addEventListener('submit', function() {
                localStorage.removeItem(saveKey);
            });
        }
    });
}

// 검색 하이라이트
function highlightSearchTerm(term) {
    if (!term) return;
    
    const posts = document.querySelectorAll('.post');
    posts.forEach(post => {
        const html = post.innerHTML;
        const regex = new RegExp(`(${term})`, 'gi');
        post.innerHTML = html.replace(regex, '<mark>$1</mark>');
    });
}
