// For new category
$("#new_cat").click(function (e) {
  Swal.fire({
    title: "Enter New Category",
    input: "text",
    inputAttributes: {
      autocapitalize: "off",
    },
    showCancelButton: true,
    confirmButtonText: "Create",
    showLoaderOnConfirm: true,
    preConfirm: (category_name) => {
      return fetch(`/category/new`, {
        body: JSON.stringify({ category_name: category_name }),
        method: "POST",
      })
        .then((res) => res.json())
        .then((response) => {
          console.log(response.category_error);
          if (response.category_error) {
            throw new Error(response.category_error);
          } else if (response.category_created) {
            Swal.fire(`${response.category_created}`);
            setInterval(function () {
              window.location.reload();
            }, 1000);
          }
        })
        .catch((error) => {
          Swal.showValidationMessage(`${error}`);
        });
    },
    allowOutsideClick: () => !Swal.isLoading(),
  }).then((result) => {
    if (result.category_created) {
      Swal.fire(`${result.category_created}`);
    }
  });
});

// For new category
$("#new_tag").click(function (e) {
  Swal.fire({
    title: "Enter New Tag",
    input: "text",
    inputAttributes: {
      autocapitalize: "off",
    },
    showCancelButton: true,
    confirmButtonText: "Create",
    showLoaderOnConfirm: true,
    preConfirm: (tag_name) => {
      return fetch(`/tag/new`, {
        body: JSON.stringify({ tag_name: tag_name }),
        method: "POST",
      })
        .then((res) => res.json())
        .then((response) => {
          console.log(response.tag_error);
          if (response.tag_error) {
            throw new Error(response.tag_error);
          } else if (response.tag_created) {
            Swal.fire(`${response.tag_created}`);
            setInterval(function () {
              window.location.reload();
            }, 1000);
          }
        })
        .catch((error) => {
          Swal.showValidationMessage(`${error}`);
        });
    },
    allowOutsideClick: () => !Swal.isLoading(),
  }).then((result) => {
    if (result.tag_created) {
      Swal.fire(`${result.tag_created}`);
    }
  });
});
