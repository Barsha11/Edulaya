let input_message = $("#chat-message-input");
let message_body = $(".maa");
let send_message_form = $("#send-message-form");
const USER_ID = $("#logged-in-user").val();
console.log(USER_ID);

let ws_scheme = window.location.protocol == "https:" ? "wss://" : "ws://";

let endpoint = ws_scheme + window.location.host + '/ws/chat/1/';

var socket = new WebSocket(endpoint);


function newMessage(message, sent_by_id, thread_id) {
  console.log(message, sent_by_id, thread_id);
  if ($.trim(message) === "") {
    return false;
  }
  let message_element;
  let chat_id = "chat_" + thread_id;
  if (sent_by_id == USER_ID) {
    message_element = `

    <li class="chat-left">
    <div class="chat-avatar">
        <img src="https://www.bootdey.com/img/Content/avatar/avatar3.png" alt="Retail Admin">
    </div>
    <div class="chat-text">${message}</div>
</li>
        `;
  } else {
    message_element = `
    <li class="chat-right">
    <div class="chat-text">${message}</div>
    <div class="chat-avatar">
        <img src="https://www.bootdey.com/img/Content/avatar/avatar4.png" alt="Retail Admin">
    </div>
</li>
        `;
  }

  let message_body = $('.messages-wrapper[chat-id="' + chat_id + '"] .maa');
  message_body.append($(message_element));
  message_body.animate(
    {
      scrollTop: $(document).height(),
    },
    100
  );
  input_message.val(null);
}

socket.onopen = async function (e) {
  send_message_form.on("submit", function (e) {
    e.preventDefault();
    let message = input_message.val();
    let send_to = get_active_other_user_id();
    let thread_id = get_active_thread_id();

    let data = {
      message: message,
      sent_by: USER_ID,
      send_to: send_to,
      thread_id: thread_id,
      msg_type: "text_message",
    };
    data = JSON.stringify(data);
    socket.send(data);
    $(this)[0].reset();
  });
};

socket.onmessage = async function (e) {
  console.log("message", e);
  let data = JSON.parse(e.data);
  message_fun(e);
};

socket.onerror = async function (e) {
  //console.log("error", e);
};

socket.onclose = async function (e) {
  //console.log("close", e);
};



$(".contact-li").on("click", function () {
  $(".contacts .active").removeClass("active");
  $(this).addClass("active");

  // message wrappers
  let chat_id = $(this).attr("chat-id");

  $(".messages-wrapper.is_active").removeClass("is_active");
  $('.messages-wrapper[chat-id="' + chat_id + '"]').addClass("is_active");
});

function get_active_other_user_id() {
  let other_user_id = $(".messages-wrapper.is_active").attr("other-user-id");
  other_user_id = $.trim(other_user_id);
  return other_user_id;
}

function get_active_thread_id() {
  let chat_id = $(".messages-wrapper.is_active").attr("chat-id");
  let thread_id = chat_id.replace("chat_", "");
  return thread_id;
}


//new codess from here
async function message_fun(e) {
  const data = JSON.parse(e.data);
  if(data.text){
  if(data.text.type =="chat_message"){
  let parsed = JSON.parse(data.text.text);
  let sent_by_id = parsed.sent_by;
  let thread_id = parsed.thread_id;
  let message = parsed.message;
  newMessage(message, sent_by_id, thread_id);
  }
}

}

