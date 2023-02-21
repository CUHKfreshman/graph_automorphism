// tab pane switch effect
const triggerTabList = document.querySelectorAll('#ssm-or-at-tabs button')
triggerTabList.forEach(triggerEl => {
  const tabTrigger = new bootstrap.Tab(triggerEl)

  triggerEl.addEventListener('click', event => {
    event.preventDefault();
    tabTrigger.show();
  })
})