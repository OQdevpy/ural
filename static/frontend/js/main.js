"use strict";

function __ymReachGoal(name) {
  console.log('reachGoal', name);
  ym( 35758920, 'reachGoal', name );
}

/*
Cart & Catelog
*/
(function(){
  var all_buttons = {
    'checkout': ['<button>Оформить заказ</button>', function (instance, toast) {
      window.location = '/order/';
    }]
  };
  var to;

  function animMinicart(x) {
    $('.minicart').removeClass(x + ' animated').addClass(x + ' animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
      $(this).removeClass(x + ' animated');
    });
  };

  $(document).on('change keyup', '.js-catalog-update', function(evt){
    clearTimeout(to);
    var $t = $(this);

    to = setTimeout(function(){
      $t.closest('form').submit();
    }, 666);

  })

  $(document).on('submit', '.js-catalog-form', function(evt){
    evt.preventDefault();

    var $form = $(this);
    var action = $form.attr('action');

    var buttons = [];
    $.post( action, $form.serialize(), function( data ) {
      // миникорзина
      animMinicart('tada');

      if (data.data && data.data.order_cost) {
        $('.js-order-cost').text(data.data.order_cost);
      }
      if (data.data && data.data.order_quantity) {
        $('.js-order-quantity').text(data.data.order_quantity);
      }

      // Нижний попап
      var color = 'green';

      if (data.data && data.data.buttons) {
        $.each(data.data.buttons, function(index, val) {
          buttons.push(all_buttons[val]);
        });
      }

      if (!data.status) {
        color = 'red';
        buttons = [];
      }

      iziToast.show({
          // title: data.message,
          // timeout: 65000,
          buttons: buttons,
          message: data.message,
          color: color, // blue, red, green, yellow
      });

      if ($form.attr('id') === 'send_order') {
        __ymReachGoal('order_was_sent');
      }

      // Доп действия
      setTimeout(function(){
        if (data.data && data.data.redirect) {
          window.location = data.data.redirect
        }

        if (data.data && data.data.reload) {
          window.location.reload()
        }
      }, 666);
    });
  });

  // --

  function recalc($el) {
    var $select = $el.find('select');
    if (!$select.length) { return; }

    var $price_view = $el.find('.js-product-price');
    var $sum_view = $el.find('.js-product-sum');
    var $quantity_input = $el.find('.product-quantity__input');
    var $old_price_view = $el.find('.js-product-old-price');

    var price = parseFloat($select.find('option:selected').data('price'));
    var quantity = parseInt($quantity_input.val());
    var sum = ((price * 100 * quantity) / 100).toFixed(2);
    var old_price = parseFloat($select.find('option:selected').data('oldprice'));

    $sum_view.text(sum.toLocaleString());
    $price_view.text(price.toLocaleString());

    if (old_price > 0) {
      // $old_price_view.show();
      $old_price_view.text(old_price.toLocaleString());
    } else {
      // $old_price_view.hide();
      $old_price_view.text(0);
    }
  }

  $('.product-quantity').each(function(index, el) {

      var $l = $(this).find('.product-quantity__left');
      var $r = $(this).find('.product-quantity__right');
      var $inp = $(this).find('.product-quantity__input');
      var val = parseInt($inp.val());

      function update() {
        $inp.val(val);
        $inp.trigger('change');
      }

      $l.on('click', function(evt){
        evt.preventDefault();
        // alert(1)
        if (val > 1) {
          val = val - 1;
        }
        update()
      });

      $r.on('click', function(evt){
        evt.preventDefault();
        val = val + 1;
        update()
      });

      $inp.on('change keyup', function(evt){
        if ($inp.val() < 1) {
          $inp.val(1)
        }
      })
  });

  $('.js-product-calc').each(function(index, el) {
    var $el = $(this);

    $el.find('select').on('change', function() {
      recalc($el);
    });

    $el.find('.product-quantity__input').on('change keyup', function() {
      recalc($el);
    });

    recalc($el);
  });
})();

/*
  Other
*/
jQuery(document).ready(function($) {
  var swiper = new Swiper('.certs-slider', {
      pagination: '.swiper-pagination',
      slidesPerView: 5,
      paginationClickable: true,
      spaceBetween: 30
  });

  var s = new Swiper('.slider-wrapper', {
    slidesPerView: 1,
    pagination: '.swiper-pagination',
    paginationClickable: true,
  })

  $("#callback").iziModal();
  $(document).on('click', '.modal-open', function (event) {
    event.preventDefault();
    $('#callback').iziModal('open');
  });

  // ---

  $('.js-menu-toggle').click(function(event) {
    $('.main-menu').toggleClass('main-menu_active');
    $(this).toggleClass('mobile-menu-toggle_active');
  });

  //--

  $('.category-menu-toggle__btn').click(function(event) {
    $(this).toggleClass('category-menu-toggle__btn_active');
    $('.sidebar').slideToggle(400);
  });

  // --

  function galleryImageTemplate(src) {
    return '<img class="gallery-popup-image" src="' + src + '" alt="..." />';
  }

  var gallery_cache = {};

  $('[data-gallery-open]').on('click', function(event) {
    event.preventDefault();
    // $("#modal-ajax").iziModal('open');
    $( $(this).data('gallery-open') ).iziModal('open');
  });

  $(".gallery-popup").iziModal({
    width: 640,
    radius: 5,
    padding: 20,
    group: 'gallery',
    loop: true,
    onOpening: function(modal){


      if (gallery_cache[modal.$element.data('image')]) {
        // modal.stopLoading();
        // modal.$element.find('.iziModal-content').html(galleryImageTemplate(modal.$element.data('image')));
      } else {
        modal.startLoading();
        $.get(modal.$element.data('image'), function(data) {
          modal.$element.find('.iziModal-content').html(galleryImageTemplate(modal.$element.data('image')));
          modal.stopLoading();
          gallery_cache[modal.$element.data('image')] = true;
        });
      }


    }
  });

  $('[data-ym-goal]').on('click', function() {
    __ymReachGoal($(this).data('ym-goal'));
  });

  $(document).on('submit', '.js-form', function (evt) {
    evt.preventDefault();

    var $form = $(this);
    var action = $form.attr('action');

    $.post(action, $form.serialize(), function (data) {
      if (data.success) {
        __ymReachGoal('callback_send');
        $('#callback').iziModal('close');
      }

      alert(data.message);
    });
  });
});