$(document).ready(() => {
  const $config = $("#configuration");
  const $constraints = $("#constraints");
  const $form = $("#form");
  const $disabled = $("#disabled");

  if (localStorage.getItem("config") !== null) {
    $config.val(localStorage.getItem("config"));
  }

  if (localStorage.getItem("constraints") !== null) {
    $constraints.val(localStorage.getItem("constraints"));
  }

  let config = JSON.parse($config.val());
  let constraints = JSON.parse($constraints.val());

  $constraints.on("keyup", () => {
    try {
      constraints = JSON.parse($constraints.val());
      localStorage.setItem("constraints", $constraints.val());
    } catch (e) {}
  });

  $config.on("keyup", () => {
    try {
      config = JSON.parse($config.val());
      localStorage.setItem("config", $config.val());
      prepareForm();
    } catch (e) {}
  });

  const getSelection = () => {
    const selected = {};
    $form.find("input:checked").each((i, el) => {
      selected[el.name] = selected[el.name]
        ? [...selected[el.name], el.value]
        : [el.value];
      console.log(selected);
    });
    return selected;
  };

  const validate = async (constraints, selection) => {
    const formData = new FormData();
    formData.append("constraints", JSON.stringify(constraints));
    formData.append("selection", JSON.stringify(selection));
    try {
      result = await fetch("http://localhost:8086/validate", {
        method: "POST",
        cache: "no-cache",
        body: formData,
      }).then((response) => response.json());
      $("#output").text(JSON.stringify(result, undefined, 2));
    } catch (err) {
      console.log(err);
      return Promise.reject();
    }
    return Promise.resolve(result);
  };

  const updateValidityState = (state, fieldName = null) => {
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

  async function inputChange(ev) {
    const $this = $(this);
    console.log($this.val());
    $disabled.css({ top: 0, bottom: 0, width: "100%" });
    const result = await validate(constraints, getSelection());
    $disabled.css({ top: "", bottom: "", width: "" });
    console.log(result);
    updateValidityState(result, ev.target.name);
  }

  const prepareForm = () => {
    $form.empty();
    Object.entries(config).forEach(([name, values]) => {
      const newFieldSet = $(`<fieldset><legend>${name}</legend></fieldset>`);
      values.forEach((value) => {
        const newField = $(
          `<label class="field"><input type="checkbox" name="${name}" value="${value}"> ${value}</label>`
        );
        const newInput = $("input", newField);
        newInput.on("change", inputChange);
        newField.appendTo(newFieldSet);
      });
      $form.append(newFieldSet);
    });
  };
  prepareForm();
});
