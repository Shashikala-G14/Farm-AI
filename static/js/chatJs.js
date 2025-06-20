let prompt = document.querySelector("#prompt");
let chatContainer = document.querySelector(".chat-container");
let imagebtn = document.querySelector("#image");
let submitbtn = document.querySelector("#submit");
let image= document.querySelector("#image img");
let imageinput = document.querySelector("#image input");

let user = {
  data: null,
  file: null
};

async function generateResponse(aiChatBox, userMessage) {
  let text = aiChatBox.querySelector(".ai-chat-area");

  let payload = {
    prompt: userMessage
  };

  if (user.file) {
    payload.image = user.file;
  }

  let response =  await fetch("/generate", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    prompt: userMessage,
    image: user.file ? user.file : null
  }),
});

  let contentType = response.headers.get("content-type");

  if (contentType && contentType.includes("application/json")) {
    let data = await response.json();
    let apiResponse = data.response;
    text.innerHTML = apiResponse;
  } else {
    let text = await response.text();
    console.error("Not JSON response:", text);
  }

  chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: "smooth" });
  image.src=` data:${user.file.mime_type};base64,${user.file.data}`
    image.classList.remove("choose")
  user.file={}
}

function createChatBox(html, classes) {
  let div = document.createElement("div");
  div.innerHTML = html;
  div.classList.add(classes);
  return div;
}

function handleChatResponse(message) {
  user.data = message;
  let html = `<img src="${imageUrl}" width="10%" alt="image" id="userImg">
      <div class="user-chat-area">
      ${user.data}
      ${user.file.data?`<img src="data:${user.file.mime_type};base64,${user.file.data}" class="chooseimg"/>`:""}
      </div>`;
  prompt.value = "";
  let userChatBox = createChatBox(html, "user-chat-box");
  chatContainer.appendChild(userChatBox);

  chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: "smooth" });

  setTimeout(() => {
    let html = `<img src="${aiUrl}" width="10%" alt=" " id="aiImg">
      <div class="ai-chat-area">
       <img src="${loadUrl}" alt="" class="load" width="50px">
      </div>`;
    let aiChatBox = createChatBox(html, "ai-chat-box");
    chatContainer.appendChild(aiChatBox);
    generateResponse(aiChatBox, user.data);
  }, 600);
}

prompt.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && prompt.value.trim()) {
    handleChatResponse(prompt.value);
  }
});
// submitbtn.addEventListener("click",()=>{
//   handleChatResponse(prompt.value);
// })

imageinput.addEventListener("change", () => {
  const file = imageinput.files[0];
  if (!file) return;

  let reader = new FileReader();
  reader.onload = (e) => {
    let base64string = e.target.result.split(",")[1];
    user.file = {
      mime_type: file.type,
      data: base64string
    };
    console.log("Image added for chat:", user.file);
    image.src=` data:${user.file.mime_type};base64,${user.file.data}`
    image.classList.add("choose")
  };
  // image.src=` data:${user.file.mime_type};base64,${user.file.data}`
  reader.readAsDataURL(file);
});

imagebtn.addEventListener("click", () => {
  imageinput.click();
});
