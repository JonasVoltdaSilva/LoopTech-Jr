export function initProjects() {
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const projects = [...document.querySelectorAll('.project-card')];
  const status = document.querySelector('#project-status');

  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      const category = button.dataset.filter;
      let count = 0;

      buttons.forEach((item) => {
        const selected = item === button;
        item.classList.toggle('is-selected', selected);
        item.setAttribute('aria-pressed', String(selected));
      });

      projects.forEach((project) => {
        const visible = category === 'todos' || project.dataset.category === category;
        project.hidden = !visible;
        if (visible) count += 1;
        else project.querySelector('details').open = false;
      });

      status.textContent = `${count} ${count === 1 ? 'conceito demonstrativo exibido' : 'conceitos demonstrativos exibidos'}.`;
    });
  });
}
