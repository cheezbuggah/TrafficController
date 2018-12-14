const urlParams = new URLSearchParams( window.location.search );
const ipAddr = urlParams.get( 'ip' ) || 'localhost';
const port = urlParams.get( 'port' ) || '5678';

$( document ).ready( function() {
    let ws = new WebSocket( 'ws://' + ipAddr + ':' + port + '/' ),
        responseHolder = $( '#response-holder' ),
        btn = $( '#btn' ),
        resetBtn = $( '#reset' ),
        quitBtn = $( '#quit' ),
        queueBtn = $( '#queueTraffic' ),
        lightInput = $( '#light' );

    function disableInteractionInputs() {
        queueBtn.prop( 'disabled', true );
        quitBtn.prop( 'disabled', true );
        lightInput.prop( 'disabled', true );
        btn.prop( 'disabled', true );
    }

    ws.onerror = function ( event ) {
        responseHolder.html( 'No WebSocket connection was accepted. <span class="emoji">😭</span>' );
        disableInteractionInputs();
    };

    btn.on( 'click', function ( event ) {
        if ( ws.readyState === ws.CONNECTING ) {
            responseHolder.html( 'Not so fast! The WebSocket connection is still connecting. <span class="emoji">👿</span>' );
        } else if ( ws.readyState === ws.CLOSED || ws.readyState === ws.CLOSING ) {
            responseHolder.html( 'The WebSocket connection has been closed. <span class="emoji">😢</span>' );
            btn.prop( 'disabled', true );
        } else {
            ws.send( JSON.stringify( [] ) );
        }
    } );
    resetBtn.on( 'click', function ( event ) {
        history.go( 0 );
    } );
    quitBtn.on( 'click', function( event ) {
        if ( ws.readyState === ws.CLOSED || ws.readyState === ws.CLOSING ) {
            disableInteractionInputs();
            responseHolder.html( 'Cannot reach the server. <span class="emoji">😟</span>' );
        } else {
            ws.send( JSON.stringify( { quit: true } ) );
            quitBtn.prop( 'disabled', true );
        }
    } );
    queueBtn.on( 'click', function ( event ) {
        if ( ws.readyState === ws.CLOSED || ws.readyState === ws.CLOSING ) {
            disableInteractionInputs();
            responseHolder.html( 'Cannot reach the server. <span class="emoji">😟</span>' );
        } else {
            ws.send( JSON.stringify( [ lightInput.val() ] ) );
        }
    } );

    ws.onmessage = function ( event ) {
        const array = JSON.parse( event.data );

        if ( array['quit'] ) {
            return;
        }

        const table = $( '<table>' );

        for ( const light of array ) {
            table.append(
                $( '<tr>' ).append(
                    $( '<td>' ).text( light.light ),
                    $( '<td>' ).text( light.status ).attr( 'style', 'background-color: ' + light.status + ';' )
                )
            );
        }

        responseHolder.html( '' );
        responseHolder.append( table );
    };
} );
