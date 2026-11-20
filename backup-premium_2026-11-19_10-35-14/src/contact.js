export function initContact() {
  const form = document.querySelector('#contact-form');
  const service = form.elements.namedItem('service');
  const message = form.elements.namedItem('message');
  const result = document.querySelector('#brief-result');
  const status = document.querySelector('#form-status');
  const fields = [...form.querySelectorAll('input, select, textarea')];
  let brief = null;
  form.noValidate = true;
  form.querySelector('.form-submit').disabled = false;

  function getError(field) {
    const value = field.value.trim();
    if (!value) {
      return {
        name: 'Informe seu nome.',
        email: 'Informe seu e-mail.',
        service: 'Selecione um tipo de projeto.',
        message: 'Conte um pouco sobre sua ideia.',
      }[field.name];
    }
    if (field.name === 'email' && field.validity.typeMismatch) return 'Digite um e-mail válido, como voce@exemplo.com.';
    if (field.name === 'message' && value.length < 20) return 'Descreva sua ideia em pelo menos 20 caracteres.';
    return '';
  }

  function validate(field) {
    const error = getError(field);
    document.querySelector(`#${field.id}-error`).textContent = error;
    if (error) field.setAttribute('aria-invalid', 'true');
    else field.removeAttribute('aria-invalid');
    return !error;
  }

  fields.forEach((field) => {
    field.addEventListener('blur', () => {
      if (field.value || field.hasAttribute('aria-invalid')) validate(field);
    });
    field.addEventListener('input', () => {
      if (field.hasAttribute('aria-invalid')) validate(field);
      if (field === message) {
        document.querySelector('#message-count').textContent = `${field.value.length} / 2000`;
      }
    });
    field.addEventListener('change', () => {
      if (field.hasAttribute('aria-invalid')) validate(field);
    });
  });

  function showForm(focus = false) {
    result.hidden = true;
    form.hidden = false;
    status.textContent = '';
    if (focus) form.elements.namedItem('name').focus();
  }

  document.querySelectorAll('[data-service]').forEach((link) => {
    link.addEventListener('click', () => {
      showForm();
      service.value = link.dataset.service;
      validate(service);
      status.textContent = `Assunto selecionado: ${service.selectedOptions[0].textContent}.`;
    });
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const validity = fields.map(validate);
    const firstInvalid = validity.indexOf(false);

    if (firstInvalid !== -1) {
      status.textContent = 'Revise os campos indicados antes de gerar seu resumo.';
      fields[firstInvalid].focus();
      return;
    }

    brief = {
      Nome: form.elements.namedItem('name').value.trim(),
      'E-mail': form.elements.namedItem('email').value.trim(),
      Projeto: service.selectedOptions[0].textContent,
      Ideia: message.value.trim(),
    };

    const summary = document.querySelector('#brief-summary');
    summary.replaceChildren();
    for (const [label, value] of Object.entries(brief)) {
      const term = document.createElement('dt');
      const description = document.createElement('dd');
      term.textContent = label;
      description.textContent = value;
      summary.append(term, description);
    }

    form.hidden = true;
    result.hidden = false;
    status.textContent = 'Resumo gerado nesta página. Nenhuma informação foi enviada.';
    document.querySelector('#result-title').focus();
  });

  document.querySelector('#edit-brief').addEventListener('click', () => showForm(true));

  document.querySelector('#download-brief').addEventListener('click', () => {
    if (!brief) return;
    const text = [
      'LOOP TECH JR. — RESUMO DE PROJETO',
      '',
      'Gerado localmente. Este arquivo não foi enviado à equipe.',
      '',
      ...Object.entries(brief).map(([label, value]) => `${label}: ${value}\n`),
    ].join('\r\n');
    const url = URL.createObjectURL(new Blob(['\ufeff', text], { type: 'text/plain;charset=utf-8' }));
    const link = document.createElement('a');
    link.href = url;
    link.download = 'looptech-resumo-do-projeto.txt';
    document.body.append(link);
    link.click();
    link.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    status.textContent = 'Download do resumo solicitado. Nenhuma informação foi enviada à equipe.';
  });
}
