window.updateValidityState = (state, config, fieldName = null) => {
  Object.entries(config).forEach(([name, values]) => {
    const $input = $(`input[name="${name}"]`);
    $input.each((i, el) => {
      const validValues = state[el.name] || [];
      if (!validValues.includes(el.value)) {
        $(el).prop("disabled", true);
      } else {
        $(el).prop("disabled", false);
      }
    });
  });
};
