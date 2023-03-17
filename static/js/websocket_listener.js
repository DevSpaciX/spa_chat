const roomName = JSON.parse(document.getElementById('json-roomid').textContent);
      const userName = JSON.parse(document.getElementById('json-username').textContent);
      const userImageDom = document.querySelector('#user-avatar');
      const chatSocket = new WebSocket(
          `ws://${window.location.host}/ws/${roomName}/`
      );

      chatSocket.onclose = function (e) {
          if (chatSocket.readyState !== WebSocket.OPEN) {
              console.log('WebSocket is already in CLOSING or CLOSED state.');
          }
      };

      chatSocket.onmessage = function (e) {
          const data = JSON.parse(e.data);
          if (data.message || (data.file && !data.message)) {
              let fileHtml = '';
              if (data.file && data.file.endsWith('.txt')) {
                  fileHtml =
                      `<div>
                          <a href="${data.file}" download>
                            <img src="/media/images/Circle-icons-folder.svg.png" style="height: 50px; width: 50px; margin-right: 5px;" alt="">
                          </a>
                      </div>`;
              }
              const messageHtml =
                  `<div style="display: flex; align-items: center;">
                <img style="width: 50px;height: 50px;border-radius: 50%; margin-right: 5px" src="${data.avatar}">
<b>${data.username}</b>: ${data.message}${data.answer ? `<button style="float:right; margin-left: 5px;" class="ml-4 px-2 py-1 rounded-md text-sm font-medium text-gray-700 bg-gray-100" disabled>New answer!</button>` : ''}<br>${data.file ? `
                    ${fileHtml}
                    ${data.file.endsWith('.txt') ? '' : `
                    <a class="fancybox" href="${data.file}">
                        <img style="border-radius: 10%; margin-left: 10px;" src="${data.file}">
                    </a>`}    ` : ''}
            </div>`;
              document.querySelector('#chat-messages').insertAdjacentHTML('beforeend', messageHtml);
          } else if (data.error) {
              alert(data.error);
          }
      };

      document.querySelector('#chat-message-input').focus();
      document.querySelector('#chat-message-input').addEventListener('keyup', function (e) {
          if (e.keyCode === 13) {
              document.querySelector('#chat-message-submit').click();
          }
      });

      document.querySelector('#chat-message-submit').addEventListener('click', function (e) {
          e.preventDefault();

          const messageInputDom = document.querySelector('#chat-message-input');
          const userFileDom = document.querySelector('#chat-file-input');
          const message = messageInputDom.value;
          const userFile = userFileDom.files[0];
          const answerDom = document.querySelector('#chat-reply-to-input')
          const answer = answerDom.value
          console.log(answer)

          const data = {
              'message': message,
              'username': userName,
              'room': roomName,
              'userImage': userImageDom.src,
              'answer_to': answer,
          };

          if (userFile) {
              const fileReader = new FileReader();
              fileReader.onload = function (event) {
                  const fileContentArray = new Uint8Array(event.target.result);
                  data.file = {
                      'name': userFile.name,
                      'type': userFile.type,
                      'size': userFile.size,
                      'content': Array.from(fileContentArray)
                  };
                  chatSocket.send(JSON.stringify(data));
              };

              fileReader.readAsArrayBuffer(userFile);
          } else if (message) {
              chatSocket.send(JSON.stringify(data));
          }

          messageInputDom.value = '';
          userFileDom.value = '';
      });