(function($){
$(function(){
  if($.fn.countUp) $('.counter').countUp();
  $('.progress-wrap3').each(function(){var w=$(this),p=w.data('progress-percent')/100;w.find('.progress-bar3').stop().animate({left:p*w.width()},2500);});
  if($.fn.niceSelect) $('select:not(.ds-native)').niceSelect();
  $('#ce-toggle').on('click',function(){$('.plan-toggle-wrap').toggleClass('active');});
  $('#ce-toggle').on('change',function(){var y=$(this).is(':checked');$('.tab-content #monthly').toggle(!y);$('.tab-content #yearly').toggle(y);});
  if($.fn.owlCarousel) $('.testomonial2-carousel-area').owlCarousel({loop:true,margin:30,nav:false,dots:true,smartSpeed:1300,autoplay:true,autoplayTimeout:4000,autoplayHoverPause:true,responsive:{0:{items:1},600:{items:2},1000:{items:3}},onInitialized:function(){$('.owl-dot').each(function(i){$(this).attr('aria-label','Show FAQ group '+(i+1))});}});
  var hdr=function(){$('.header-area').toggleClass('sticky',$(window).scrollTop()>=1);};$(window).on('scroll',hdr);hdr();
  var path=document.querySelector('.progress-wrap path');
  if(path){var L=path.getTotalLength();path.style.strokeDasharray=L+' '+L;path.style.strokeDashoffset=L;
    var up=function(){var s=$(window).scrollTop(),h=$(document).height()-$(window).height();path.style.strokeDashoffset=L-(s*L)/h;$('.progress-wrap').toggleClass('active-progress',s>50);};
    $(window).on('scroll',up);up();
    $('.progress-wrap').on('click',function(e){e.preventDefault();$('html, body').animate({scrollTop:0},550);});}
  $('.mobile-nav-icon').on('click',function(){$('.mobile-sidebar').addClass('mobile-menu-active');});
  $('.menu-close, .mobile-nav-list a').on('click',function(){$('.mobile-sidebar').removeClass('mobile-menu-active');});
  var want=new URLSearchParams(location.search).get('service');
  var EMAIL='info@toromovers.com';
  $('form.diler-form').on('submit',function(e){
    e.preventDefault();var f=this,$m=$(f).find('.dzFormMsg'),$b=$(f).find('[type=submit]').prop('disabled',true);
    $m.html('<div class="alert-success">Sending...</div>');
    fetch(f.action,{method:'POST',headers:{Accept:'application/json'},body:new FormData(f)}).then(function(r){return r.json()}).then(function(j){if(!j.success)throw 0;
      $m.html('<div class="alert-success">Thank you. Your message has been received. Diler Services will respond by email.</div>');f.reset();})
    .catch(function(){var l=[];new FormData(f).forEach(function(v,k){if(['access_key','subject','from_name','botcheck'].indexOf(k)<0&&v)l.push(k+': '+v)});
      $m.html('<div class="alert-danger">The message could not be sent. Please <a href="mailto:'+EMAIL+'?subject='+encodeURIComponent('Website inquiry: Diler Services')+'&body='+encodeURIComponent(l.join('\n'))+'">email '+EMAIL+'</a> instead.</div>');})
    .then(function(){$b.prop('disabled',false)});
  });
});
window.addEventListener('load',function(){if(window.AOS)AOS.init({once:true,duration:900});});
})(jQuery);
