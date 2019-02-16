$(document).ready(function() {
  $('.input').on('focus', function() {
    $('.login').addClass('clicked');
  });
  $('.login').on('submit', function(e) {
    e.preventDefault();
    $('.login').removeClass('clicked').addClass('loading');
  });
  $('.resetbtn').on('click', function(e){
      e.preventDefault();
    $('.login').removeClass('loading');
  });

  //Sign up class
  $('.input1').on('focus', function() {
    $('.logon').addClass('zoom');
    $('.login').addClass('zoom_set')
    $('.adhar').addClass('zoom_set')
    $('.login').removeClass('clicked')
  });
  $('.logon').on('submit', function(e) {
    e.preventDefault();
    $('.logon').removeClass('clicked_logon').addClass('loading');
  });
  $('.resetbtn').on('click', function(e){
      e.preventDefault();
    $('.logon').removeClass('loading');
  });
  // $('.logon').hover(function(){
  //   $('.logon').addClass('zoom');
  // })

  //Adhar Class
  // $('.input').on('focus', function() {
  //   $('.adhar').addClass('clicked1');
  // });
  $('.adhar').on('submit', function(e) {
    e.preventDefault();
    $('.adhar').removeClass('clicked1').addClass('loading');
  });
  $('.resetbtn').on('click', function(e){
      e.preventDefault();
    $('.adhar').removeClass('loading');
  });
});