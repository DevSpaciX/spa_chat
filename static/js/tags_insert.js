  function insertTag(tagStart, tagEnd) {
    const messageInput = document.querySelector('#chat-message-input');
    const startPos = messageInput.selectionStart;
    const endPos = messageInput.selectionEnd;
    const selectedText = messageInput.value.substring(startPos, endPos);
    const newText = messageInput.value.slice(0, startPos) + tagStart + selectedText + tagEnd + messageInput.value.slice(endPos);
    messageInput.value = newText;
    messageInput.focus();
    messageInput.setSelectionRange(startPos + tagStart.length, endPos + tagStart.length);
  }