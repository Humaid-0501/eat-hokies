$(document).ready(function(){
    //Sign-in form validation
    $("#Sign-up").submit(function(event){
        var username = $("#email").val();
        var password = $("#password").val();
        var email_message = $('<p class="email-error"}">Please provide a valid username</p>');
        var pass_message = $('<p class="pass-error"}">Please provide a password</p>');

        // Checking for blank fields.
        if(username ==='' && password ===''){
            $('.email-error').remove();
            $('.pass-error').remove();
            $('input[type="username"],input[type="password"]').css({"border": "2px solid darkred"});
            $('.email-label').append(email_message);
            $('.pass-label').append(pass_message);
            alert("Please fill all the fields");
            event.preventDefault();
        }
        else if(username=='' || email.length<3){
            $('.email-error').remove();
            $('input[type="username"]').css("border","2px solid darkred");
            $('input[type="password"]').css("border", "none");
            $('.email-label').append(email_message);
            $('.pass-error').remove();
            alert("Please provide a valid email")
            event.preventDefault();
        }
        else if(password==''){
            $('.pass-error').remove();
            $('.pass-label').append(pass_message);
            $('input[type="password"]').css("border","2px solid darkred");
            $('input[type="username"]').css("border", "none");
            $('.email-error').remove();
            alert("Please provide a password");
            event.preventDefault();
        }
        else{
            // alert("Log-in successful!");
        }
    });


    //check query string
    checkQueryString();


    // Quantity update - increase
    $('div.item-quantity a.plus-button').click(function(){
        var itemQuantity = parseInt($(this).siblings('p.quantity').text());
        var item_id = $(this).attr('data-item-id');
        var ajax_url = $(this).attr('data-ajax-url');
        // Using the core $.ajax() method
        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                item_id: item_id
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType : "json",

            headers: {'X-CSRFToken': csrftoken},

            context: this
        })
          // Code to run if the request succeeds (is done);
          // The response is passed to the function
          .done(function( json ) {
              // alert("request received successfully");
              if(json.success == 'success'){
                  var itemQuantity = $(this).siblings('p.quantity');
                  var amount = $('.cart-button').find('.item-price span.amount');
                  // console.log(amount);
                  var new_quantity = json.quantity;
                  var new_price = json.price;
                  // console.log(new_price);
                  $(itemQuantity).text(new_quantity);
                  $(amount).text(new_price);
                  var successMessage = $('<p class="quantity-success">Quantity and price are successfully updated!</p>');
                  $(successMessage).appendTo($('.plus-button')).fadeOut(800 , function(){
                      $(this).remove();
                  });
              }
              else{
                  alert("Error:" + json.error);
              }

          })
          // Code to run if the request fails; the raw request and
          // status codes are passed to the function
          .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
          })
          // Code to run regardless of success or failure;
          .always(function( xhr, status ) {
            // alert( "The request is complete!" );
          });
    });

    // Quantity update - decrease
    $('div.item-quantity a.minus-button').click(function(){
        var itemQuantity = parseInt($(this).siblings('p.quantity').text());
        var item_id = $(this).attr('data-item-id');
        var ajax_url = $(this).attr('data-ajax-url');
        // Using the core $.ajax() method
        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                item_id: item_id
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType : "json",

            headers: {'X-CSRFToken': csrftoken},

            context: this
        })
          // Code to run if the request succeeds (is done);
          // The response is passed to the function
          .done(function( json ) {
              // alert("request received successfully");
              if(json.success == 'success'){
                  var itemQuantity = $(this).siblings('p.quantity');
                  var amount = $('.cart-button').find('.item-price span.amount');
                  var new_quantity = json.quantity;
                  var new_price = json.price;
                  $(itemQuantity).text(new_quantity);
                  $(amount).text(new_price);
                  var successMessage = $('<p class="quantity-success">Quantity and price are successfully updated!</p>');
                  $(successMessage).appendTo($('.plus-button')).fadeOut(800 , function(){
                      $(this).remove();
                  });
              }
              else{
                  alert("Error:" + json.error);
              }

          })
          // Code to run if the request fails; the raw request and
          // status codes are passed to the function
          .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
          })
          // Code to run regardless of success or failure;
          .always(function( xhr, status ) {
            // alert( "The request is complete!" );
          });
    });


    //add to cart
    $('div.item-quantity button.cart-button').on("click", function(){
        var cartMessage = $(this).parent('div.item-description h1');
        // console.log(cartMessage);
        var successMessage = $('<p class="cart-success">Successfully added to your cart!</p>');
        // $('.item-quantity').append(successMessage);
        $(successMessage).appendTo($('.item-description')).fadeOut(1200 , function(){
            $(this).remove();
        });
    });

    // Comments
    var check_view_comment = false;

    $('.view-comment').click(function (){

        if(!check_view_comment){

            var username = $(this).attr('data-user-name');
            var item_id = $(this).attr('data-item-id');
            var ajax_url = $(this).attr('data-ajax-url');

            // Using the core $.ajax() method
            $.ajax({

                // The URL for the request
                url: ajax_url,

                // The data to send (will be converted to a query string)
                data: {
                    _id: item_id
                },

                // Whether this is a POST or GET request
                type: "GET",

                headers: {'X-CSRFToken': csrftoken},

                // The type of data we expect back
                dataType: "json",

                context: this
            })
                // Code to run if the request succeeds (is done);
                // The response is passed to the function
                .done(function (json) {
                    //alert("request received successfully")
                    if (json.success == 'success') {
                        if (json.review.length == 0) {
                            var newCommentFormat = `<div class = "comments-recorded"> <p class="user-comment-recorded">No comments available.</p>
                            </div>`;

                            $(".user-commented").append(newCommentFormat);
                            check_view_comment = true;
                        }
                        else{
                            for (i=0; i<json.review.length; i++){
                                if(username == json.review[i].user || json.review[i].role == "admin"){
                                    var newCommentFormat = `<div class = "comments-recorded"> <p class="user-comment-recorded"> ${json.review[i].review} </p>
                                    <p class="user-comment-time">Commented on: ${json.review[i].date}</p>
                                    <p>Commented By: <a href="/users/profile/${json.review[i].user}">${json.review[i].user}</a></p>
                                    <input type="hidden" class="hidden-id" value="${json.review[i].id}">
                                    <button class="edit-button">Edit</button>
                                    <button class="delete-button">Delete</button> </div>`;
                                }
                                else{
                                    var newCommentFormat = `<div class = "comments-recorded"> <p class="user-comment-recorded"> ${json.review[i].review} </p>
                                    <p class="user-comment-time">Commented on: ${json.review[i].date}</p>
                                    <p>Commented By: <a href="/users/profile/${json.review[i].user}">${json.review[i].user}</a></p>
                                    <input type="hidden" class="hidden-id" value="${json.review[i].id}"></div>`;

                                }

                                $(".user-commented").append(newCommentFormat);
                                check_view_comment = true;
                            }
                        }
                    }

                })
                // Code to run if the request fails; the raw request and
                // status codes are passed to the function
                .fail(function (xhr, status, errorThrown) {
                    alert("Sorry, there was a problem!");
                    console.log("Error: " + errorThrown);

                })
                // Code to run regardless of success or failure;
                .always(function (xhr, status) {
                    // alert("The request is complete!");
                });
        }
    });

    var userCommentID = 1
    //Edit Comment
    $('.user-commented').on('click', '.edit-button', function (){
       var userCommentElement = $("#createUserComment");
       let existingComment =$(this).siblings(('.user-comment-recorded')).html();
       userCommentElement.val(existingComment);
       editCommentHTMLElement = $(this).parent();
       userCommentID = $(this).siblings(('.hidden-id')).val();
    });

    //User Interaction - 1: on Submit button a new element will be
    //added and modifying an existing element
    var editCommentHTMLElement = false;

    $('.user-commented').on('click', '.delete-button', function (){
       var comment_id = $(this).siblings(".hidden-id").val();
       // var ajax_url = $(this).attr('data-ajax-url2');
        $.ajax({

            // The URL for the request
            url: "/eatHokies/comment/delete",

            // The data to send (will be converted to a query string)
            data: {
                _comment_id: comment_id,
            },

            // Whether this is a POST or GET request
            type: "POST",

            headers: {'X-CSRFToken': csrftoken},

            // The type of data we expect back
            dataType: "json",

            context: this
        })
        .done(function (json) {
                $(this).siblings().remove();
                $(this).remove();
            })
            // Code to run if the request fails; the raw request and
            // status codes are passed to the function
            .fail(function (xhr, status, errorThrown) {
                alert("Sorry, there was a problem!");
                alert(url)
                console.log("Error: " + errorThrown);

            })
            // Code to run regardless of success or failure;
            .always(function (xhr, status) {
                // alert("The request is complete!");
            });
    });

    $(".submit-button").click(function(){

        var createUserCommentElement = $("#createUserComment");
        var userComment = createUserCommentElement.val();

        //if the comment length is zero then alert the user when
        //clicking on submit button
        if(userComment.length <= 0){
            alert('No Comment added');
        }
        //if the comment is already posted then comment will either be added or modified
        else {
            let commentDate = (new Date()).toLocaleString('en-US');

            if(!editCommentHTMLElement) {


                var item_id = $(this).attr('data-item-id');
                var ajax_url = $(this).attr('data-ajax-url');

                // Using the core $.ajax() method
                $.ajax({

                    // The URL for the request
                    url: ajax_url,

                    // The data to send (will be converted to a query string)
                    data: {
                        _id: item_id,
                        _user_review: $("#createUserComment").val()
                    },

                    // Whether this is a POST or GET request
                    type: "POST",

                    headers: {'X-CSRFToken': csrftoken},

                    // The type of data we expect back
                    dataType: "json",

                    context: this
                })
                    // Code to run if the request succeeds (is done);
                    // The response is passed to the function
                    .done(function (json) {
                        //alert("request received successfully")
                        if (json.success == 'success') {
                            for (i=0; i<json.comment.length; i++){
                                var newCommentFormat = `<div class = "comments-recorded"> <p class="user-comment-recorded"> ${json.comment[i].review} </p>
                                <p class="user-comment-time">Commented on: ${json.comment[i].date}</p>
                                 <input type="hidden" class="hidden-id" value="${json.comment[i].id}">
                                <p>Commented By: <a href="/users/profile/${json.comment[i].user}">${json.comment[i].user}</a></p>
                                <button class="edit-button">Edit</button>
                                <button class="delete-button">Delete</button></div>`;
                            }
                            $(".user-commented").append(newCommentFormat);
                        }

                    })
                    // Code to run if the request fails; the raw request and
                    // status codes are passed to the function
                    .fail(function (xhr, status, errorThrown) {
                        alert("Sorry, there was a problem!");
                        console.log("Error: " + errorThrown);

                    })
                    // Code to run regardless of success or failure;
                    .always(function (xhr, status) {
                        // alert("The request is complete!");
                    });
            }

            else{
                editCommentHTMLElement.find('.user-comment-recorded').html(userComment);


                let notifySuccess = $('<p class = ".user-comment"> Comment edited successfully</p>');

                //successfully EDITED comment message for users
                $(notifySuccess).appendTo($(".user-comment")).fadeOut('slow', function(){
                        $(this).remove();
                });

                var comment_id = userCommentID;
                var ajax_url = $(this).attr('data-ajax-url2');
                $.ajax({

                    // The URL for the request
                    url: ajax_url,

                    // The data to send (will be converted to a query string)
                    data: {
                        _comment_id: comment_id,
                        _new_comment: userComment
                    },

                    // Whether this is a POST or GET request
                    type: "POST",

                    headers: {'X-CSRFToken': csrftoken},

                    // The type of data we expect back
                    dataType: "json",

                    context: this
                })
                .done(function (json) {
                        alert("request received successfully")
                    })
                    // Code to run if the request fails; the raw request and
                    // status codes are passed to the function
                    .fail(function (xhr, status, errorThrown) {
                        alert("Sorry, there was a problem!");
                        console.log("Error: " + errorThrown);

                    })
                    // Code to run regardless of success or failure;
                    .always(function (xhr, status) {
                        // alert("The request is complete!");
                    });
            }
            editCommentHTMLElement = false;
            createUserCommentElement.val("");
        }

    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function checkQueryString(){
    var querystring = window.location.search;
    // console.log(querystring);
    var urlParams = new URLSearchParams(querystring);
    if(urlParams.has('search-items')){
        var keyword = urlParams.get("search-items").toLowerCase();
        if(keyword == 'burger'){
            var searchedItem = $('<div class="searched-item">' +
                    '<div>' +
                    '   <a href="details.html">\n' +
                    '   <div>' +
                    '   <img src="img/burger_meal_1.jpeg" alt="Food Image" style="width: 100%;"> <!--Source of image: https://www.google.com/imghp?hl=en-->\n' +
                    '   <div class="item-description">\n' +
                    '   <h4>Haystack Tavern Double</h4>\n' +
                    '   <p>10 mins</p>\n' +
                    '   <p class="price">$ 9.5</p>\n' +
                    '   </div>' +
                    '    </div>' +
                    '   \n' +
                    '   </a>' +
                    '</div>' +
                    '<div>' +
                    '   <a href="details.html">\n' +
                    '   <img src="img/burger_2.jpeg"  style="width: 100%;" alt="Food Image"> <!--Source of image: https://www.google.com/imghp?hl=en-->\n' +
                    '   <div class="item-description">\n' +
                    '   <h4>Mighty Meaty Burger</h4>\n' +
                    '   <p>10 mins</p>\n' +
                    '   <p class="price">$ 10</p>\n' +
                    '   </div>\n' +
                    '   </a>' +
                    '</div>' +
                    '<div>\n' +
                '                        <a href="details.html">\n' +
                '                            <img src="img/burger_3.jpeg"  style="width: 100%;" alt="Food Image"> <!--Source of image: https://www.google.com/imghp?hl=en-->\n' +
                '                        <div class="item-description">\n' +
                '                            <h4>Bean Burger</h4>\n' +
                '                            <p>7 mins</p>\n' +
                '                            <p class="price">$ 7.5</p>\n' +
                '                        </div>\n' +
                '                        </a>\n' +
                '                    </div>'+
                '   <div>\n' +
                '                        <a href="details.html">\n' +
                '                            <img src="img/burger_4.jpeg"  style="width: 100%;" alt="Food Image"> <!--Source of image: https://www.google.com/imghp?hl=en-->\n' +
                '                        <div class="item-description">\n' +
                '                            <h4>Chicken Teriyaki</h4>\n' +
                '                            <p>8 mins</p>\n' +
                '                            <p class="price">$ 8.5</p>\n' +
                '                        </div>\n' +
                '                        </a>\n' +
                '                    </div>'+
                '</div>');
            $(".search-items").append(searchedItem);
            window.alert("You searched burger");
        }
        else if(keyword=='rice'){
            var searchedItem = $('<div class="searched-item">' +
                '<div>\n' +
                '                        <a href="details.html">\n' +
                '                                <img src="img/Chicken-Rice-bowl.jpeg"  style="width: 100%;" alt="Food Image"> <!--Source of image: https://www.google.com/imghp?hl=en-->\n' +
                '                            <div class="item-description">\n' +
                '                                <h4>Chicken Rice Bowl</h4>\n' +
                '                                <p>8 mins</p>\n' +
                '                                <p class="price">$ 8.5</p>\n' +
                '                            </div>\n' +
                '                        </a>\n' +
                '                    </div>\n' +
                '\n' +
                '                    <div>\n' +
                '                        <a href="details.html">\n' +
                '                                <img src="img/Asian-Chicken-Rice-bowl.jpeg" style="width: 100%;" alt="Food Image"> <!--Source of image: https://www.google.com/imghp?hl=en-->\n' +
                '                            <div class="item-description">\n' +
                '                                <h4>Asian Rice Bowl</h4>\n' +
                '                                <p>9 mins</p>\n' +
                '                                <p class="price">$ 8.5</p>\n' +
                '                            </div>\n' +
                '                        </a>\n' +
                '                    </div>' +
                '</div>');
            $(".search-items").append(searchedItem);
            window.alert("You searched rice");
        }
        else if(keyword=='sandwich'){
            var searchedItem = $('<div class="searched-item">' +
                '<div>\n' +
                '                        <a href="details.html">\n' +
                '                                <img src="img/Mayonnaise-sandwich.jpeg"  style="width: 100%;" alt="Food Image"> <!--Source of image: https://www.google.com/imghp?hl=en-->\n' +
                '                            <div class="item-description">\n' +
                '                                <h4>Mayo Sandwich</h4>\n' +
                '                                <p>5 mins</p>\n' +
                '                                <p class="price">$ 5</p>\n' +
                '                            </div>\n' +
                '                        </a>\n' +
                '                    </div>\n' +
                '\n' +
                '                    <div>\n' +
                '                        <a href="details.html">\n' +
                '                                <img src="img/chicken_sandwich.webp"  style="width: 100%;" alt="Food Image"> <!--Source of image: https://www.google.com/imghp?hl=en-->\n' +
                '                            <div class="item-description">\n' +
                '                                <h4>Chicken Sandwich</h4>\n' +
                '                                <p>6 mins</p>\n' +
                '                                <p class="price">$ 6</p>\n' +
                '                            </div>\n' +
                '                        </a>\n' +
                '                    </div>' +
                '</div>');
            $(".search-items").append(searchedItem);
            window.alert("You searched sandwich");
        }
        else{
            var noItem = $('<h2>No items found</h2>');
            $('.search-items').append(noItem);
            window.alert("No items found");
        }
    }

}