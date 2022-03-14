"use strict";

this.ckan.module('cookie_banner', function ($) {
  return {
    initialize: function () {

      var banner = this.el

      function _toggleCookieBanner() {
        banner.toggleClass('hidden')
      }

      function acceptCookieNotice() {
        // Set cookie for 1 year
        document.cookie = 'accept-cookie-policy=1; path=/; samesite=lax; max-age=' + (60*60*24*365)
        _toggleCookieBanner()
      }
      
      // If cookie isn't set, show the banner
      if (!document.cookie.split('; ').find(row => row.trim().startsWith('accept-cookie-policy'))) {
        _toggleCookieBanner()
      }

      banner.find('button#accept-cookie-policy').on("click", function() {
        acceptCookieNotice()
      })
    }
  }
})