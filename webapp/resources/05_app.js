window.updateValidityState = (state, config, fieldName = null) => {
  console.log("dsfdsfdsfds");
  Object.entries(config).forEach(([name, values]) => {
    const $input = $(`input[name="${name}"]`);
    $input.each((i, el) => {
      const validValues = state[el.name] || [];
      const $field = $(el).closest(".field");
      if (validValues.includes(el.value)) {
        $field.get(0).classList.add("valid");
      } else {
        $field.get(0).classList.remove("valid");
      }
    });
  });
};
