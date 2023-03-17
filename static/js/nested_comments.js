var marginIncrease = 20;
var nestedComments = document.querySelectorAll('.nested-comment');
var marginLeft = 21;
for (var i = 1; i < nestedComments.length; i++) {
    nestedComments[i].style.marginLeft = marginLeft + 'px';
    marginLeft += marginIncrease;
}