function replyMessage(messageId) {
  document.getElementById('chat-reply-to-input').value = messageId;
  var username = document.getElementById('chat-message-'+messageId+'-username').textContent;
  document.getElementById('chat-message-input').value = '@'+username+' ';
  document.getElementById('chat-message-input').focus();
}