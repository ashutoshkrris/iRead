function showNotifications() {
  const container = document.getElementById("notification-container");
  if (container.classList.contains("d-none")) {
    container.classList.remove("d-none");
  } else {
    container.classList.add("d-none");
  }
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function removeNotification(removeNotificationURL, notificationId) {
  const csrftoken = getCookie("csrftoken");
  fetch(`${removeNotificationURL}`, {
    method: "DELETE",
    headers: {
      "X-CSRFToken": csrftoken,
    },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.error) {
        new Notify({
          title: "Error",
          text: "Something went wrong.",
          status: "error",
        });
      } else {
        const container = document.getElementById(`noti_${notificationId}`);
        container.classList.add("d-none");
        $("#noti_count").html(
          `<i class="fa fa-bell" aria-hidden="true"></i> ${data.noti_count}`
        );
      }
    });
}
