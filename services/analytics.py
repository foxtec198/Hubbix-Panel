from models.clients import Client

def get_analytics_code(client:Client) -> None | str:
    codes = [] # Cria as TAGS que vão ser utilizados
    if client: # Confirma se foi passo o cliente
        if client.gtag: # Confirma se tem GTAG code
            codes.append(f"""
                <!-- GOOGLE TAG -->
                <script async src="https://www.googletagmanager.com/gtag/js?id={client.gtag}"></script>
                <script>
                    window.dataLayer = window.dataLayer || [];
                    function gtag(){{dataLayer.push(arguments);}}
                    gtag('js', new Date());
                    gtag('config', '{client.gtag}');
                </script>

                <!-- Event snippet for WhatsApp --> 
                <script> 
                    function gtag_report_conversion(url) {{ var callback = function () {{ if (typeof(url) != 'undefined') {{ window.location = url; }} }}; 
                    gtag('event', 'conversion', {{ 'send_to': '{client.gtag}/2KRvCNH83qgaEJSJubgB', 'event_callback': callback }}); return false; }}
                </script>
                <!-- END GOOGLE TAG -->
            """.strip())

        if client.pixel:# Confirma se tem pixel code
            codes.append(f"""
                <!-- META PIXEL -->
                <script>
                    !function(f,b,e,v,n,t,s)
                    {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
                    n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
                    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
                    n.queue=[];t=b.createElement(e);t.async=!0;
                    t.src=v;s=b.getElementsByTagName(e)[0];
                    s.parentNode.insertBefore(t,s)}}(window, document,'script',
                    'https://connect.facebook.net/en_US/fbevents.js');
                    fbq('init', '{client.pixel}');
                    fbq('track', 'PageView');
                </script>
                <!-- END META PIXEL -->
            """.strip())
    return "\n".join(codes)
