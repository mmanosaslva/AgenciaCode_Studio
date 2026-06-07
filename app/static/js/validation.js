function setupFieldValidation(formId, config) {
    var form = document.getElementById(formId);
    if (!form) return;
    var submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) submitBtn.disabled = true;

    config.forEach(function(field) {
        var el = document.getElementById(field.id);
        if (!el) return;

        var errEl = el.parentElement.querySelector('.field-error-msg');
        if (!errEl) {
            errEl = document.createElement('div');
            errEl.className = 'field-error-msg';
            el.parentElement.appendChild(errEl);
        }

        if (field.blockNumeric) {
            el.addEventListener('keypress', function(e) {
                if (e.key < '0' || e.key > '9') {
                    if (e.key !== '+' && e.key !== 'Backspace' && e.key !== 'Tab' && e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') {
                        e.preventDefault();
                    }
                }
            });
        }

        function validateField() {
            var val = el.value.trim();
            if (field.lower) el.value = val.toLowerCase();
            if (field.trimmed !== false) el.value = val;

            var valid = true;
            var msg = '';
            if (el.required && !val) {
                valid = false;
                msg = 'Este campo es obligatorio';
            } else if (field.pattern && val && !new RegExp(field.pattern).test(val)) {
                valid = false;
                msg = field.errorMsg || 'Formato invalido';
            } else if (field.custom && val) {
                var result = field.custom(val);
                valid = result.valid;
                msg = result.msg;
            }

            el.classList.remove('field-valid', 'field-invalid');
            errEl.classList.remove('visible');
            errEl.textContent = '';
            if (val && valid) {
                el.classList.add('field-valid');
            } else if (val && !valid) {
                el.classList.add('field-invalid');
                errEl.textContent = msg;
                errEl.classList.add('visible');
            }
            checkFormValidity(form, submitBtn);
        }

        el.addEventListener('blur', validateField);
        el.addEventListener('input', function() {
            el.classList.remove('field-valid', 'field-invalid');
            errEl.classList.remove('visible');
            errEl.textContent = '';
            checkFormValidity(form, submitBtn);
        });
        el.addEventListener('change', validateField);
    });

    form.addEventListener('submit', function(e) {
        config.forEach(function(field) {
            var el = document.getElementById(field.id);
            if (el) el.value = el.value.trim();
        });
        if (submitBtn && submitBtn.disabled) {
            e.preventDefault();
        }
    });
}

function checkFormValidity(form, btn) {
    if (!btn) return;
    var valid = true;
    var fields = form.querySelectorAll('input, select, textarea');
    fields.forEach(function(f) {
        if (f.hasAttribute('required') && !f.value.trim()) valid = false;
        if (f.classList.contains('field-invalid')) valid = false;
    });
    btn.disabled = !valid;
    if (btn.disabled) {
        btn.title = 'Completa todos los campos correctamente';
    } else {
        btn.title = '';
    }
}
