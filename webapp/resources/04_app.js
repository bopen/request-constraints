window.updateValidityState = (state, config, fieldName = null) => {
  Object.entries(config).forEach(([name, values]) => {
    const $input = $(`input[name="${name}"]`);
    if (fieldName === name) {
      return;
    }
    $input.each((i, el) => {
      const validValues = state[el.name] || [];
      const $field = $(el).closest(".field");
      if (!validValues.includes(el.value)) {
        $field.get(0).classList.add("invalid");
      } else {
        $field.get(0).classList.remove("invalid");
      }
    });
  });
};
