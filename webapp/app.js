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

  $constraints.on("change", () => {
    constraints = JSON.parse(ev.target.value);
    localStorage.setItem("constraints", ev.target.value);
  });

  $config.on("change", (ev) => {
    console.log("ssss");
    config = JSON.parse(ev.target.value);
    localStorage.setItem("config", ev.target.value);
    prepareForm();
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
      result = fetch("http://localhost:8086/validate", {
        method: "POST",
        cache: "no-cache",
        body: formData,
      }).then((response) => response.json());
    } catch (err) {
      console.log(err);
      return Promise.reject();
    }
    return Promise.resolve(result);
  };

  const updateValidityState = (state, fieldName = null) => {
    Object.entries(state).forEach(([name, validValues]) => {
      const $input = $(`input[name="${name}"]`);
      $input.each((i, el) => {
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
