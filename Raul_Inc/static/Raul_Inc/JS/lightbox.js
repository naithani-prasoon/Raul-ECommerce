function Lightbox( parameters ){
    var query = parameters.query;

    //Lightbox components
    var $background, $main, $holder, $preloader, $center, $mask, $description, $description_text, $image;

    //Initial and final animation
    var from, fromAmount, to, toAmount, returnToInitial;

    //Initial sizes
    var initial_width, initial_height;

    //Max Size Percentage
    var maxWidth, maxHeight, enlarging, enlargable;

    //transitions times
    var tempTransition, inImageTime, outImageTime;
    var buttonsDisabledAlpha, buttonsInactiveAlpha, infinite;

    var descriptionLocation, descriptionPosition;
    //buttons
    var buttons = new Array();
    var groups = new Array();
    var $elements = $(query);
    var numContents = $elements.length, current, current_mult = 0, current_group;

    //main holder
    var mainPadding;
    var timer, refreshRate = 30;
    var currentScroll = 0, scrollerEase=8;
    var scrollTop, closing = false, fixed = false;

    function updateElements(){
        $elements = $(query);
        buttons = new Array();
        groups = new Array();
        $elements.each(function(index){
            $(this).attr("num", index);
            buttons[index] = new Object();
            buttons[index].href = $(this).attr("href");

            if($(this).attr("width") && $(this).attr("height")){
                buttons[index].forceSize = true;
                buttons[index].width = $(this).attr("width");
                buttons[index].height = $(this).attr("height");
            }
            else
                buttons[index].forceSize = false;

            if( $(this).attr("rel") ){
                var rel = $(this).attr("rel");

                if(existsGroup(rel))
                    addToGroup(rel, index);
                else
                    addGroup(rel, index);

                buttons[index].rel = rel;
            }
            else
                buttons[index].rel = false;

            buttons[index].iframe = false;
            if( $(this).attr("iframe") )
                if( $(this).attr("iframe") == "true" )
                    buttons[index].iframe = true;

            buttons[index].autoResize = true;
            if( $(this).attr("autoresize") )
                if( $(this).attr("autoresize") == "false" )
                    buttons[index].autoResize = false;

            buttons[index].description = $(this).attr("description");

            $(this).unbind('click');
            $(this).click(openLightbox);
        });
    }


    this.loadNewConfig = function(xml){
        buttons = new Array();
        groups = new Array();
        $background.remove();
        $main.remove();
        parseXml(xml);
    }

    this.refreshButtons = function(){
        updateElements();
    }

    //PARSE XML AND BUILDS ELEMENTS
    $.ajax({
        type: "GET",
        url: parameters.config,
        dataType: "xml",
        success: parseXml
    });
    function parseXml(xml){
        var configuration = $(xml).find("configuration");

        tempTransition = parseInt($(configuration).find("transitionTime").text(), 10);
        from = $(configuration).find("from").text();
        fromAmount = parseInt($(configuration).find("fromAmount").text(), 10);
        to = $(configuration).find("to").text();
        toAmount = parseInt($(configuration).find("toAmount").text(), 10);
        returnToInitial = $(configuration).find("returnToInitial").text();
        inImageTime = parseInt($(configuration).find("inImageTime").text(), 10);
        outImageTime = parseInt($(configuration).find("outImageTime").text(), 10);
        var backClose = $(configuration).find("backClose").text();
        buttonsDisabledAlpha = parseFloat($(configuration).find("buttonsDisabledAlpha").text(), 10);
        buttonsInactiveAlpha = parseFloat($(configuration).find("buttonsInactiveAlpha").text(), 10);
        infinite = $(configuration).find("infinite").text();
        maxWidth = parseFloat($(configuration).find("maxWidth").text(), 10);
        maxHeight = parseFloat($(configuration).find("maxHeight").text(), 10);

        //--------------------------------------------------------------------------------
        //BACKGROUND COVER
        $background = $('<div class="lightbox_background"></div>');
        var background_cover = $(configuration).find("background_cover");
        var color = $(background_cover).find("color").text();
        var color_alpha = $(background_cover).find("color_alpha").text();
        var pattern = $(background_cover).find("pattern").text();

        //	main attributes
        $background.css({	"zoom" : "1",
            "width": "100%",
            "height": "100%",
            "position" : "fixed",
            "top":"0px"
        });

        if(backClose == "true")
            $background.click(closeLightbox);

        processColorAndPattern($background, color, color_alpha, pattern);

        //--------------------------------------------------------------------------------
        //MAIN HOLDER
        $main = $('<div class="lightbox_main"></div>');
        $holder = $('<div class="lightbox_holder"></div>');
        $center = $('<div class="lightbox_center"></div>');

        if(backClose == "true"){
            $main_hit_area = $('<div class="lightbox_main_hit"></div>');
            $main.append($main_hit_area);
            $main_hit_area.css({	"width": "100%",
                "height":"100%",
                "position" : "absolute"
            });
            $main_hit_area.click(closeLightbox);
        }

        var lightbox_main = $(configuration).find("lightbox_main");
        var color = $(lightbox_main).find("color").text();
        var color_alpha = $(lightbox_main).find("color_alpha").text();
        var pattern = $(lightbox_main).find("pattern").text();
        var round_corners = $(lightbox_main).find("round_corners").text();
        var padding = parseInt($(lightbox_main).find("padding").text(), 10);
        initial_width = parseInt($(lightbox_main).find("initial_width").text(), 10);
        initial_height = parseInt($(lightbox_main).find("initial_height").text(), 10);

        //	main attributes
        $main.css({	"width": "100%",
            "height":"100%",
            "position" : "absolute"
        });

        $holder.css({	"width": initial_width,
            "position" : "relative",
            "-webkit-border-radius" : round_corners+"px",
            "-moz-border-radius" : round_corners+"px",
            "-o-border-radius" : round_corners+"px",
            "border-radius" : round_corners+"px",
            "padding" : padding+"px",
            "overflow" : "hidden"
        });
        $center.css({	"width": initial_width+padding*2,
            "position" : "relative",
            "margin" : "0 auto",
            "top" : "50%",
            "margin-top" : -initial_height/2-padding
        });



        mainPadding = padding;
        processColorAndPattern($holder, color, color_alpha, pattern);


        //--------------------------------------------------------------------------------
        //PRELOADER
        $preloader = $('<div class="lightbox_preloader"></div>');

        var preloader = $(configuration).find("preloader");
        var preloader_image = $(preloader).find("preloader").text();
        var preloader_width = $(preloader).find("preloader_width").text();
        var preloader_height = $(preloader).find("preloader_height").text();

        if(preloader_image != "none"){
            $preloader.css({	"width" : preloader_width,
                "height" : preloader_height,
                "background-image" : "url("+preloader_image+")",
                "background-repeat" : "no-repeat",
                "margin" : "0 auto",
                "top" : "50%",
                "position" : "absolute",
                "margin-top" : -preloader_height/2
            });
        }


        //--------------------------------------------------------------------------------
        //MASK
        $mask = $('<div class="lightbox_mask"></div>');
        $image = $('<div class="lightbox_image"></div>');

        var lightbox_mask = $(configuration).find("lightbox_image_mask");
        var color = $(lightbox_mask).find("color").text();
        var color_alpha = $(lightbox_mask).find("color_alpha").text();
        var pattern = $(lightbox_mask).find("pattern").text();
        var round_corners = $(lightbox_mask).find("round_corners").text();

        $mask.css({	"width": initial_width,
            "height": initial_height,
            "-webkit-border-radius" : round_corners+"px",
            "-moz-border-radius" : round_corners+"px",
            "-o-border-radius" : round_corners+"px",
            "border-radius" : round_corners+"px",
            "position" : "relative",
            "float": "left",
            "overflow":"hidden"
        });
        $image.css({	"position": "absolute" });

        processColorAndPattern($mask, color, color_alpha, pattern);


        //--------------------------------------------------------------------------------
        //DESCRIPTION
        $description = $('<div class="lightbox_description"></div>');
        $description_text = $('<div class="lightbox_text">This is a description</div>');

        var description = $(configuration).find("description");
        //	text
        var font_family = $(description).find("font_family").text();
        var font_color = $(description).find("font_color").text();
        var font_size = $(description).find("font_size").text();
        var font_weight = $(description).find("font_weight").text();
        var text_align = $(description).find("text_align").text();		// -> left / center / right
        //	background
        var background = $(description).find("background").text();
        var color = $(description).find("color").text();
        var color_alpha = $(description).find("color_alpha").text();
        var pattern = $(description).find("pattern").text();
        var round_corners = $(description).find("round_corners").text();
        var paddingTopBottom = $(description).find("paddingTopBottom").text();
        var paddingLeftRight = $(description).find("paddingLeftRight").text();
        var back_size = $(description).find("back_size").text();		// -> fit / max
        //	positioning
        var location = $(description).find("location").text(); // -> inside / outside / inside-image
        descriptionLocation = location;
        var position = $(description).find("position").text();		// -> bottom / top
        descriptionPosition = position;
        var align = $(description).find("align").text();		// -> left / center / right
        //margins
        var top = $(description).find("top").text();
        var bottom = $(description).find("bottom").text();
        var left = $(description).find("left").text();
        var right = $(description).find("right").text();

        //	background attributes
        if(background == "true")
            processColorAndPattern($description_text, color, color_alpha, pattern);
        $description.css({	"position":"relative",
            "text-align" : align
        });



        //	text attributes
        $description_text.css({	"clear" : "all",
            "-webkit-border-radius" : round_corners+"px",
            "-moz-border-radius" : round_corners+"px",
            "-o-border-radius" : round_corners+"px",
            "border-radius" : round_corners+"px",
            "padding" : (paddingTopBottom+"px "+paddingLeftRight+"px"),
            "font-family" : font_family,
            "color" : font_color,
            "font-size" : font_size+"px",
            "font-weight" : font_weight,
            "position" : "relative",
            "text-align" : text_align,
            "margin-top" : top+"px",
            "margin-bottom" :bottom+"px",
            "margin-left" :left+"px",
            "margin-right" :right+"px"
        });

        if(back_size == "fit")
            $description_text.css({	"display":"inline-block" });
        else if(back_size == "max")
            $description.css({	"width": "100%"  });

        if(location == "inside-image" && position == "bottom")
            $description.css({	"top": "100%" });


        $description.append($description_text);


        //--------------------------------------------------------------------------------
        //APPENDS
        $mask.append($image);
        switch(location){
            case "inside":
                if(position == "top")
                    $holder.append($description, $mask);
                else
                    $holder.append($mask, $description);

                $center.append($holder);
                break;
            case "outside":
                if(position == "top")
                    $center.append($description, $holder);
                else
                    $center.append($holder, $description);

                $holder.append($mask);
                break;
            case "inside-image":
                $center.append($holder);
                $holder.append($mask);
                $mask.append($description);
                break;
        }
        $main.append($center);
        if(preloader_image != "none")
            $holder.append($preloader);


        //--------------------------------------------------------------------------------
        //BUTTONS
        var buttons_xml = $(xml).find("buttons");
        $(buttons_xml).find("button").each(function(index){
            var $this = $(this);

            //action
            var action = $this.find("action").text();

            //size
            var width = $this.find("width").text();
            var height = $this.find("height").text();

            //states
            var normal = $this.find("normal").text();
            var over = $this.find("over").text();

            //positioning
            var vertical_align = $this.find("vertical_align").text();
            var horizontal_align = $this.find("horizontal_align").text();
            var top = $this.find("top").text();
            var bottom = $this.find("bottom").text();
            var left = $this.find("left").text();
            var right = $this.find("right").text();

            //lightbox_close || lightbox_next || lightbox_previous
            var $link = $('<a class="lightbox_'+action+'" href="#"></a>');

            var $button = $('<div class="lightbox_button" normal="'+normal+'" over="'+over+'"></div>');
            $button.css({	"width" : width ,
                "height" : height,
                "position" : "absolute"
            });

            buttonsClass($button);

            $('span.hover', $button).css({	"width" : width ,
                "height" : height,
                "position" : "absolute"
            });

            $link.css({	"width" : width ,
                "height" : height,
                "position" : "absolute",
                "margin-top" : top+"px",
                "margin-left" :left+"px"
            });


            $link.append($button);

            if(horizontal_align == "right")
                $link.css({ "left":"100%" });
            else if(horizontal_align == "left")
                $link.css({ "left": -width });
            else if(horizontal_align == "center")
                $link.css({ "left": "50%",
                    "margin-left" : (parseInt(left, 10)-parseInt(width, 10)/2)+"px"});


            if(vertical_align == "bottom")
                $link.css({ "top" : "100%" });
            else if(vertical_align == "top")
                $link.css({ "top": -height });
            else if(vertical_align == "center")
                $link.css({ "top": "50%",
                    "margin-top" : (parseInt(top, 10)-parseInt(height, 10)/2)+"px"});

            $center.append($link);

            if(action == "close")
                $link.click(closeLightbox);
            else if(action == "next")
                $link.click(nextImage);
            else if(action == "previous")
                $link.click(previousImage);
            else if(action == "enlarge")
                $link.click(enlargeImage);
        });

        //add lightbox to document
        $('body').append($background);
        $('body').append($main);
        $background.fadeOut(0);
        $main.fadeOut(0);
        $image.fadeTo(0, 0);
        $description.fadeTo(0, 0);

        if(location == "inside-image" && position == "bottom")
            $description.css({	"margin-top": -$($description).height() });

        updateElements();
    }
    ////////////////////////////////



    //GROUPS MANAGE FUNCTIONS
    function addToGroup(name, num){
        for(var i=0; i<groups.length ; i++)
            if( groups[i].rel == name)
                groups[i].elements.push(num);
    }

    function existsGroup(name){
        for(var i=0; i<groups.length ; i++)
            if( groups[i].rel == name)
                return true;
        return false;
    }

    function addGroup(name, num){
        var groupObj = new Object();

        groupObj.rel = name;
        groupObj.elements = new Array();
        groupObj.elements.push(num);

        groups.push(groupObj);
    }

    function positionInGroup(groupNum, num){
        for(var f=0; f < groups[groupNum].elements.length ; f++)
            if( groups[groupNum].elements[f] == num)
                return f;

        return false;
    }

    function getGroup(name){
        for(var i=0; i<groups.length ; i++)
            if( groups[i].rel == name)
                return i;
        return false;
    }

    function lengthGroup(groupNum){
        return groups[groupNum].elements.length;
    }

    function elementNumGroup(groupNum, elemNum){
        return groups[groupNum].elements[elemNum];
    }
    ////////////////////////////////



    //OPENS LIGHTBOX
    function openLightbox(){
        //var href = $(this).attr("href");
        current = $(this).attr("num");

        //alert(buttons[current].rel);
        if(buttons[current].rel){
            current_group = getGroup(buttons[current].rel);
            numContents = lengthGroup(current_group);
            current_mult = positionInGroup(current_group, current);
        }
        else{
            numContents=1;
            current_mult = 0;
            $('a.lightbox_previous>div', $main).fadeTo(tempTransition, buttonsInactiveAlpha);
            $('a.lightbox_next>div', $main).fadeTo(tempTransition, buttonsInactiveAlpha);
        }
        //add Lightbox
        $background.stop().fadeIn(tempTransition);
        $main.stop().fadeIn(tempTransition);

        scrollTop = $(window).scrollTop();
        currentScroll = scrollTop;
        $main.css('top', Math.round(scrollTop)+"px");

        timer = setTimeout(updatePosition, refreshRate);

        openContent(true);

        return false;
    }
    function updatePosition(){
        if(!fixed)
            scrollTop = $(window).scrollTop();

        var mover = ((scrollTop-currentScroll)/scrollerEase);
        currentScroll += mover;

        $main.css('top', Math.round(currentScroll)+"px");
        timer = setTimeout(updatePosition, refreshRate);
    }
    ////////////////////////////////



    //OPENS CONTENT INTO THE LIGHTBOX
    function openContent(initial){
        var href = buttons[current].href;
        var forceSize = buttons[current].forceSize;
        var iframe = buttons[current].iframe;
        var autoResize = buttons[current].autoResize;

        if(!enlarging)
            fixed = false;
        else
            enlarging = false;

        enlargable = false;
        $('a.lightbox_enlarge', $main).stop().fadeOut(500);

        //lightbox_close || lightbox_next || lightbox_previous
        if(infinite != "true" && numContents != 1){
            if(current_mult == 0)
                disableButton($('a.lightbox_previous>div', $main));
            else
                enableButton($('a.lightbox_previous>div', $main));

            if(current_mult == numContents-1)
                disableButton($('a.lightbox_next>div', $main));
            else
                enableButton($('a.lightbox_next>div', $main));
        }

        var object = new Object();
        object.initial = initial;
        object.forceSize = forceSize;
        object.autoResize = autoResize;

        if(forceSize){
            if(buttons[current].width[buttons[current].width.length-1] != '%')
                object.width = parseInt(buttons[current].width, 10);
            else
                object.width = $(window).width() * (parseFloat(buttons[current].width, 10)/100.0);

            if(buttons[current].height[buttons[current].height.length-1] != '%')
                object.height = parseInt(buttons[current].height, 10);
            else
                object.height = $(window).height() * (parseFloat(buttons[current].height, 10)/100.0);

            if(object.height > $(window).height())
                fixed = true;
        }

        if(!autoResize)
            fixed = true;

        if(isImage(href)){
            openImage(href, object);
        }
        else if(iframe){
            openIframe(href, object);
        }
        else if(isHtml(href)){
            openAjax(href, object);
        }
        else if(isSwf(href)){
            openSwf(href, object);
        }
        else if(isYoutube(href)){
            var id = getVideoId(href);
            openIframe("http://youtube.com/embed/"+id, object);
        }
        else if(isVimeo(href)){
            var id = getVideoId(href);
            openIframe("http://player.vimeo.com/video/"+id, object);
        }
        else if(isDaily(href)){
            var id = getVideoId(href);
            openIframe("http://www.dailymotion.com/embed/video/"+id, object);
        }
    }
    ////////////////////////////////


    //OPENS SWF CONTENT
    function openSwf(url, vars){
        var $obj = $('<object id="player1" width="'+vars.width+'" height="'+vars.height+'" name="player1"><param name="movie" value="'+url+'" /><param name="allowfullscreen" value="true" /><param name="scale" value="noScale" /><param name="salign" value="lt" /><param name="allowscriptaccess" value="always" /><param name="flashvars" value="path=deuter" /><embed id="player1" width="'+vars.width+'" wmode="transparent" height="'+vars.height+'" src="'+url+'" flashvars="path=deuter" allowfullscreen="true" allowscriptaccess="always" name="player1" scale="noScale" salign="lt"></embed></object>');
        //Animate
        animateEntrance($obj, vars);
    }
    ////////////////////////////////


    //OPENS IFRAME CONTENT
    function openIframe(url, vars){
        var $iframe = $('<iframe src="'+url+'" type="text/html" wmode="transparent" scrolling="auto" width="'+vars.width+'" height="'+vars.height+'" frameborder="0" allowfullscreen></iframe>');

        //Animate
        animateEntrance($iframe, vars);
    }
    ////////////////////////////////


    //OPENS AJAX CONTENT
    function openAjax(url, vars){
        var $ajax = $('<div></div>');
        $ajax.load(url);

        //Animate
        animateEntrance($ajax, vars);
    }
    ////////////////////////////////


    //OPENS IMAGES
    function openImage(url, vars){
        //create image
        var $obj = $('<div></div>');
        $obj.css("position", "absolute");
        var img = new Image();
        img.onload = function() {
            $obj.append(img);
            if(vars.forceSize){
                var minWidth = vars.width;
                var minHeight = vars.height;

                var ratio = 1;

                ratio = img.width / minWidth;

                if( img.height / ratio < minHeight ){
                    ratio = img.height / minHeight;
                    $obj.css("left", -((img.width / ratio)-minWidth)/2);
                }
                else
                    $obj.css("top", -((img.height / ratio)-minHeight)/2);

                img.width /= ratio;
                img.height /= ratio;
            }
            else{
                var maxWidthImage =  $( window ).width() * maxWidth -  mainPadding*2;
                var maxHeightImage = $( window ).height() * maxHeight -  mainPadding*2;

                if(fixed){
                    if( img.width > maxWidthImage){
                        var ratio = (img.width / maxWidthImage);
                        img.width /= ratio;
                        img.height /= ratio;
                    }
                    if(vars.autoResize){
                        $('a.lightbox_enlarge', $main).stop().fadeIn(500);
                        enlargable = true;
                    }
                }
                else{
                    // If larger than permited
                    if( img.width > maxWidthImage || img.height > maxHeightImage ) {
                        var ratio = 1;

                        if( img.width > maxWidthImage )
                            ratio = img.width / maxWidthImage;

                        if( img.height > maxHeightImage && ratio < (img.height/maxHeightImage))
                            ratio = img.height / maxHeightImage;

                        img.width /= ratio;
                        img.height /= ratio;

                        if(ratio > 1){
                            $('a.lightbox_enlarge', $main).stop().fadeIn(500);
                            enlargable = true;
                        }
                    }
                }

                //Final Size
                var widthImage = img.width;
                var heightImage = img.height;

                vars.width = widthImage;
                vars.height = heightImage;
            }

            //Animate
            animateEntrance($obj, vars);
        };
        img.src = url;
    }
    ////////////////////////////////



    //ANIMATES AND ADDS AN ALREADY PROCESSED CONTENT TO THE LIGHTBOX
    function animateEntrance($obj, vars){
        if(vars.initial && from != "none" && from != undefined){
            if(from=="top")
                $center.css( { "margin-top" : (-vars.height/2-mainPadding*2-fromAmount) });
            else if(from=="bottom")
                $center.css( { "margin-top" : (-vars.height/2-mainPadding*2+fromAmount) });
        }
        else if(vars.initial)
            $center.css( { "margin-top" : (-vars.height/2-mainPadding*2) });

        //Check over border
        if(fixed){
            var windowHeight = $( window ).height();
            var bodyHeight = $( document ).height();

            var plus = vars.height - windowHeight;
            if(vars.height > windowHeight){
                if(scrollTop-plus/2 < 0)
                    scrollTop = plus/2 + mainPadding*2;
                if(scrollTop+windowHeight+plus/2 > bodyHeight)
                    scrollTop = bodyHeight - windowHeight - plus/2 - mainPadding*2;
            }

        }

        //animations
        $holder.animate( {
            'width': vars.width+'px'
        } , tempTransition);
        $center.animate( {
                'width': (vars.width+mainPadding*2)+'px',
                "margin-top" : (-vars.height/2-mainPadding*2)+'px'},
            {duration: tempTransition,
                step: function() {
                    $center.css("overflow","visible");
                },

                complete: function() {
                    $center.css("overflow","visible");
                }
            });
        $mask.animate( {
                'width': vars.width+'px',
                'height': vars.height+'px'
            } , tempTransition ,
            function(){
                $image.append($obj);
                $image.fadeTo(inImageTime, 1);
                $preloader.fadeTo(tempTransition, 0);

                if(buttons[current].description != undefined){
                    $description_text.html(buttons[current].description);
                    $description.fadeTo(tempTransition, 1);

                    if(descriptionLocation == "inside-image" && descriptionPosition == "bottom")
                        $description.css({	"margin-top": -$description.height() });

                }
                fadeIE($image, inImageTime, 1);
            });
    }
    ////////////////////////////////



    //CHANGE CONTENT TO CURRENT
    function changeContent(){
        $preloader.fadeTo(tempTransition, 1);
        $description.fadeTo(tempTransition, 0);
        fadeIE($image, outImageTime, 0);
        $image.fadeTo(outImageTime, 0, function(){
            $('*', $image).remove();
            openContent(false);
        });
    }
    ////////////////////////////////



    //NEX AND PREVIOUS FUNCTIONS
    function nextImage(){
        if(current_mult < (numContents-1)){
            current_mult++;
            current = elementNumGroup(current_group, current_mult);
            changeContent();
        }
        else if(infinite == "true"){
            current_mult=0;
            current = elementNumGroup(current_group, current_mult);
            changeContent();
        }
        return false;
    }

    function previousImage(){
        if(current_mult > 0){
            current_mult--;
            current = elementNumGroup(current_group, current_mult);
            changeContent();
        }
        else if(infinite == "true"){
            current_mult=(numContents-1);
            current = elementNumGroup(current_group, current_mult);
            changeContent();
        }
        return false;
    }
    ////////////////////////////////


    //ENLARGE IMAGE FUNCTION
    function enlargeImage(){
        if(enlargable){
            if(!fixed){
                fixed = true;
                enlarging = true;
            }
            else
                fixed = false;
            changeContent();
        }
        return false;
    }
    ////////////////////////////////



    //CLOSES THE LIGHTBOX
    function closeLightbox(){
        if(!closing){
            closing = true;
            clearTimeout(timer);

            $background.fadeOut(tempTransition);
            $main.fadeOut(tempTransition, removeLightbox);
            $description.fadeTo(tempTransition, 0);

            if(to=="top")
                $center.animate( { "margin-top" : "+="+(-toAmount) } , tempTransition);
            else if(to=="bottom")
                $center.animate( { "margin-top" : "+="+(toAmount) } , tempTransition);
        }

        return false;
    }

    function removeLightbox(){
        $('*', $image).remove();
        if(returnToInitial == "true"){
            $holder.css( { 'width': initial_width+'px'});
            $center.stop().css( { 	'width': (initial_width+mainPadding*2),
                'margin-top' : (-initial_height/2-mainPadding*2)
            });
            $mask.css( { 'width': initial_width+'px', 'height': initial_height+'px'});
        }
        $preloader.fadeTo(0, 1);
        $image.fadeTo(0, 0);
        closing = false;
    }
    ////////////////////////////////


    //BUTTONS ENABLE AND DISABLE FUNCTIONS
    function disableButton($obj){
        $obj.fadeTo(500, buttonsDisabledAlpha);
        $obj.addClass("disabled");
        $("span.hover", $obj).stop().fadeTo(500, 0);
    }
    function enableButton($obj){
        $obj.fadeTo(500, 1);
        $obj.removeClass("disabled");
    }
    ////////////////////////////////

    //HELPING FUNCTIONS
    function processColorAndPattern(object, color, alpha, pattern){
        //	color attributes
        if(alpha != "0" && alpha != 0){
            var filter = getFilter(color, alpha);
            var rgba = getRGBA(color, alpha);

            object.css({	"background-color" : color,
                "filter" : filter,
                "background" : rgba
            });

        }
        //	pattern attributes
        if(pattern != "none")
            object.css({	"background-image" : "url("+pattern+")",
                "background-repeat" : "repeat"
            });
    }

    function getFilter(color, alpha){
        var color_alpha = parseInt((parseFloat(alpha, 10)*255)).toString(16);
        var filter = "progid:DXImageTransform.Microsoft.gradient(startColorstr=#"+color_alpha+color.substring(1, 3)+color.substring(3, 5)+color.substring(5, 7)+
            ",endColorstr=#"+color_alpha+color.substring(1, 3)+color.substring(3, 5)+color.substring(5, 7)+")";

        return filter;
    }

    function getRGBA(color, alpha){
        var rgba = "rgba("+color.substring(1, 3)+", "+color.substring(3, 5)+", "+color.substring(5, 7)+", "+alpha+")";
        return rgba;
    }

    function isImage(str){
        var type = (str.substr(str.length-3));

        if(type == "jpg" || type == "png" || type == "gif")
            return true;

        return false;
    }

    function isHtml(str){
        var type = (str.substr(str.length-4));
        var type1 = (str.substr(str.length-3));

        if(type == "html")
            return true;

        if(type1 == "php")
            return true;

        return false;
    }

    function isSwf(str){
        var type = (str.substr(str.length-3));

        if(type == "swf")
            return true;

        return false;
    }

    function isYoutube(str){
        var type = (str.substr(0, 7));

        if(type == "youtube")
            return true;

        return false;
    }

    function isVimeo(str){
        var type = (str.substr(0, 5));

        if(type == "vimeo")
            return true;

        return false;
    }

    function isDaily(str){
        var type = (str.substr(0, 11));

        if(type == "dailymotion")
            return true;

        return false;
    }

    function getVideoId(str){
        var i=0;
        while(str[i] != ':')
            i++;

        return str.substr(i+1);
    }

    //fade out object for IE 8 and lower
    var isIE = jQuery.browser.msie;
    var brVersion = jQuery.browser.version;
    function fadeIE($obj, time, to){
        if(isIE && brVersion <= 8)
            $('*', $obj).each(function(){
                $(this).stop().fadeTo(time, to);
            });
    }
};