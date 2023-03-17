function replyMessage(messageId) {
    document.getElementById('chat-reply-to-input').value = messageId;
    document.getElementById('chat-message-input').focus();
}