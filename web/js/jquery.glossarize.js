/**
 * Plugin Name: Glossarizer
 * Author : Vinay @Pebbleroad
 * Date: 20/09/2013
 * Description: Takes glossary terms from a JSON object -> Searches for terms in your html -> Wraps a abbr tag around the matched word
 */

;(function($){

  /**
   * Defaults
   */
  
  var pluginName = 'glossarizer',
    defaults = {
      sourceURL     : '', /* URL of the JSON file with format {"term": "", "description": ""} */
      termData      : '', /* Use Either sourceURL or termData: */
      replaceTag    : 'abbr', /* Matching words will be wrapped with abbr tags by default */
      lookupTagName : 'p, ul', /* Lookup in either paragraphs or lists. Do not replace in headings */
      callback      : null, /* Callback once all tags are replaced: Call or tooltip or anything you like */
      replaceOnce   : true /* Replace only once in a TextNode */
    }

  /**
   * Constructor
   */
  
  function Glossarizer(el, options){

    var base = this

    base.el = el;
    base.$el            = $(el)
    base.options        = $.extend({}, defaults, options)

    /* Collection of terms */
    base.terms = []

    /* Collection of Descriptions */
    base.descriptions = []

    /**
     * Regex Tags
     */
    
    base.regexOption = base.options.replaceOnce? 'i': 'ig';
    
    
    /*
    Check if sourceURL is set. If not use termData
     */
    
    if(base.options.sourceURL){

      $.getJSON(this.options.sourceURL).then(function(data){
      
        // Push Terms and definitions to Array        
        base.setTermData(data)

      })

    }else{

      base.setTermData(this.options.termData)

    }
    

  }

  /**
   * Prototypes
   */
  Glossarizer.prototype = {
    /**
     * Converts glossary source in an terms and descriptions object
     * @param {[object]} data
     */
    setTermData: function(data){

      for(var i = 0; i< data.length; i++){
        
        this.terms.push(data[i].term)
        this.descriptions.push(data[i].description)

      }

      this.wrapTerms()

    },
    
    /**
     * Wraps the matched terms by calling traverser     
     */
    wrapTerms: function(){
      
      var nodes = this.el.querySelectorAll(this.options.lookupTagName),
          tag = '<strong rel="tipsy">',
          html = '',
          self = this

      for(var i =0; i < nodes.length; i++){
        self.traverser(nodes[i])
      }      

      /**
       * Callback
       */
      
      if(this.options.callback) this.options.callback.call(this.$el)

    },

    /**
     * Traverses through nodes to find the matching terms in TEXTNODES
     */

    traverser: function(node){      

      var next

      if (node.nodeType === 1) {

        /*
         Element Node
         */

        if (node = node.firstChild) {
            //console.log('node.firstChild: ' + node.firstChild);
            do {
                // Recursively call traverseChildNodes
                // on each child node
                next = node.nextSibling

                this.traverser(node)

            } while(node = next)
        }

      } else if (node.nodeType === 3) {

        /*
         Text Node
         */

        var temp = document.createElement('div'),
            data = node.data;            

        // for each glossary term
        for(var i =0; i < this.terms.length; i++){
        	//console.log('this.terms[' + i + ']: ' + this.terms[i]);
        	

          var pattern = '\\b'+this.terms[i] + '\\b',
              re = new RegExp(pattern, this.regexOption)
          
          //console.log('data 1: (' + (data.indexOf(this.options.replaceTag) !== -1) + ')' + data);
          // text musst exist and do not contain another glossary replacement
          if(re.test(data) && !(data.indexOf(this.options.replaceTag) !== -1)){

            data = data.replace(re, 
                    '<'+this.options.replaceTag+' tabIndex="0" class="glossarizer_replaced" title="'+this.descriptions[i]+'">' + '$&' + '</'+ this.options.replaceTag+'>')

              // console.log('data 2: ' + data);
          }          
        }

        temp.innerHTML = data;
        
        
        while (temp.firstChild) {          
          node.parentNode.insertBefore(temp.firstChild, node)
        }

        node.parentNode.removeChild(node)

      }

    },

  };


  /**
   * Plugin
   * @param  {[type]} options   
   */
  $.fn[pluginName] =function(options){

    return this.each(function(){
      if(!$.data(this, 'plugin_' + pluginName)){
        $.data(this, 'plugin_' + pluginName, new Glossarizer(this, options))
      }
    });

  }


})(jQuery);