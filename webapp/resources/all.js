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

  const getSelection = (result) => {
    const selected = {};
    $form.find("input:checked").each((i, el) => {
      selected[el.name] = selected[el.name]
        ? [...selected[el.name], el.value]
        : [el.value];
      console.log(selected);
    });
    return selected;
  };

  const getRetrieveRequest = (validation) => {
    const payload = {};
    Object.keys(config).forEach((name) => {
      const $input = $(`input[name="${name}"]:checked`);
      const selected = [];
      $input.each((i, el) => {
        selected.push(el.value);
      });
      if (selected.length > 0) {
        payload[name] = selected.reduce((current, v) => {
          if (validation[name].includes(v)) {
            return [...current, v];
          }
          return current;
        }, []);
      }
    });
    return payload;
  };

  const validate = async (constraints, selection, configuration) => {
    const formData = new FormData();
    formData.append("constraints", JSON.stringify(constraints));
    formData.append("selection", JSON.stringify(selection));
    formData.append("configuration", JSON.stringify(configuration));
    let result = null;
    try {
      result = await fetch("http://localhost:8086/validate", {
        method: "POST",
        cache: "no-cache",
        body: JSON.stringify(Object.fromEntries(formData.entries())),
        headers: { "Content-Type": "application/json" },
      }).then((response) => response.json());
      $("#output").text(JSON.stringify(result, undefined, 2));
    } catch (err) {
      console.log(err);
      return Promise.reject();
    }
    return Promise.resolve(result);
  };

  async function inputChange(ev) {
    const $this = $(this);
    console.log($this.val());
    $disabled.css({ top: 0, bottom: 0, width: "100%" });
    const result = await validate(constraints, getSelection(), config);
    $disabled.css({ top: "", bottom: "", width: "" });
    console.log(result);
    window.updateValidityState(result, config, ev.target.name);
    $("#payload").text(
      JSON.stringify(getRetrieveRequest(result), undefined, 2)
    );
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
    window.initForm?.(config);
  };
  prepareForm();
});
