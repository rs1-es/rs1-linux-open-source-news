import feedparser
import datetime
import html
import os
import pytz
import func_timeout
from concurrent.futures import ThreadPoolExecutor

strings = {
    "en": {
        "lang": "en",
        "langFull": "English",
        "websiteDesc": "Javascript-free Linux/open source news aggregator",
        "entries": {
            "news": [["https://9to5linux.com/feed/atom", "9to5Linux", "https://9to5linux.com/", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://linuxiac.com/feed/", "Linuxiac", "https://linuxiac.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://distrowatch.com/news/dw.xml", "DistroWatch", "https://distrowatch.com", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://itsfoss.com/rss/", "It's FOSS", "https://itsfoss.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.gamingonlinux.com/article_rss.php", "GamingOnLinux", "https://www.gamingonlinux.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.omgubuntu.co.uk/feed", "OMG! Ubuntu!", "https://www.omgubuntu.co.uk/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://linuxsecurity.com/linuxsecurity_articles.xml", "LinuxSecurity.com", "https://linuxsecurity.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://debugpointnews.com/feed/", "DebugPoint NEWS", "https://debugpointnews.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.phoronix.com/rss.php", "Phoronix", "https://www.phoronix.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://feeds.feedburner.com/Ubuntubuzz", "Ubuntu Buzz!", "https://www.ubuntubuzz.com/", "%Y-%m-%dT%H:%M:%S.%f%z"],
            ["https://linmob.net/feed.xml", "LINMOB.net", "https://linmob.net/", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.linux-magazine.com/rss/feed/lmi_news", "Linux Magazine", "https://www.linux-magazine.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://fossforce.com/feed/", "FOSS Force", "https://fossforce.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://fullcirclemagazine.org/feed/", "Full Circle Magazine", "https://fullcirclemagazine.org/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://linuxgamingcentral.com/posts/index.xml", "Linux Gaming Central", "https://linuxgamingcentral.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://news.opensuse.org/feed.xml", "openSUSE News", "https://news.opensuse.org/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.omglinux.com/feed/", "OMG! Linux", "https://www.omglinux.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://planet.kde.org/index.xml", "Planet KDE", "https://planet.kde.org/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://lwn.net/headlines/rss", "LWN.net", "https://lwn.net/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://planet.debian.org/rss20.xml", "Planet Debian", "https://planet.debian.org/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://tuxphones.com/rss/", "TuxPhones", "https://tuxphones.com/", "%a, %d %b %Y %H:%M:%S %Z"],
            ["https://www.linuxinsider.com/rss-feed", "LinuxInsider", "https://www.linuxinsider.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://joho-todai.com/en/rss/", "Joho no Todai (English)", "https://joho-todai.com/", "%a, %d %b %Y %H:%M:%S %Z"]],
            "videos": [["https://www.youtube.com/feeds/videos.xml?channel_id=UCVls1GmFKf6WlTraIb_IaJg", "DistroTube", "https://distro.tube/", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCONH73CdRXUjlh3-DdLGCPw", "Niccolò Ve", "https://tube.kockatoo.org/c/niccolo_ve/videos", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCuHJawjMUOk4gjywwDg727w", "Riba Linux", "https://odysee.com/@Riba-Linux:5", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCld68syR8Wi-GY_n4CaoJGA", "Brodie Robertson", "https://odysee.com/@BrodieRobertson:5", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCMiyV_Ib77XLpzHPQH_q0qQ", "Veronica Explains", "https://tilvids.com/c/veronicaexplains_channel/videos", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UC5UAwBUum7CPN5buc-_N1Fw", "The Linux Experiment", "https://tilvids.com/c/thelinuxexperiment_channel/videos", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCMePQAfCxotiG_2B5qYv4aQ", "Linux User Space", "https://tilvids.com/a/linuxuserspace/videos", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://framatube.org/feeds/videos.xml?accountId=8178", "Free Software Foundation", "https://framatube.org/a/fsf/videos", "%a, %d %b %Y %H:%M:%S %Z"],
            ["https://video.retroedge.tech/feeds/videos.xml?videoChannelId=4", "RetroEdge.Tech", "https://retroedge.tech/", "%a, %d %b %Y %H:%M:%S %Z"],
            ["https://tilvids.com/feeds/videos.xml?videoChannelId=71", "Linux Lounge", "https://tilvids.com/c/linux_lounge/videos", "%a, %d %b %Y %H:%M:%S %Z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCxQKHvKbmSzGMvUrVtJYnUA", "Learn Linux TV", "https://www.learnlinux.tv/", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCoryWpk4QVYKFCJul9KBdyw", "Switched to Linux", "https://switchedtolinux.com/", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCylGUf9BvQooEFjgdNudoQg", "The Linux Cast", "https://odysee.com/@thelinuxcast:4", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCfX55Sx5hEFjoC3cNs6mCUQ", "The Linux Foundation", "https://www.youtube.com/@LinuxfoundationOrg/videos", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCNnUnr4gwyNmzx_Bbzvt29g", "LinuxScoop", "https://www.youtube.com/@linuxscoop/videos", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCc3L72F_yWWr1V1ft_CDpAA", "9to5Linux (Videos)", "https://www.youtube.com/@9to5Linux/videos", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UC1yGcBvdPGxRIMT1yo_bKIQ", "Jake@Linux", "https://www.youtube.com/@JakeLinux/videos", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCjSEJkpGbcZhvo0lr-44X_w", "TechHut", "https://www.youtube.com/@TechHut/videos", "%Y-%m-%dT%H:%M:%S%z"]],
            "more": [["https://www.linuxlinks.com/feed/", "LinuxLinks", "https://www.linuxlinks.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.fosslinux.com/feed", "FOSS Linux", "https://www.fosslinux.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://linuxtldr.com/feed/", "Linux TLDR", "https://linuxtldr.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://trendoceans.com/feed/", "TREND OCEANS", "https://trendoceans.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.linuxcapable.com/feed/", "LinuxCapable", "https://www.linuxcapable.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.cyberciti.com/atom/atom.xml", "nixCraft", "https://www.cyberciti.biz/", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.linux.com/feed/", "Linux.com", "https://www.linux.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://linuxstans.com/feed/", "Linux Stans", "https://linuxstans.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.ubuntupit.com/feed/", "UbuntuPIT", "https://www.ubuntupit.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://feeds.feedburner.com/UbuntuhandbookNewsTutorialsHowtosForUbuntuLinux", "UbuntuHandbook", "https://ubuntuhandbook.org/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.tecmint.com/feed/", "Tecmint", "https://www.tecmint.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://opensource.com/feed", "Opensource.com", "https://opensource.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.redhat.com/sysadmin/rss.xml", "Red Hat - Enable Sysadmin", "https://www.redhat.com/sysadmin/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://feeds.feedburner.com/Ostechnix", "OSTechNix", "https://ostechnix.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://fedoramagazine.org/feed/", "Fedora Magazine", "https://fedoramagazine.org/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.debugpoint.com/feed/", "DebugPoint.com", "https://www.debugpoint.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.howtoforge.com/feed.rss", "HowtoForge", "https://www.howtoforge.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://thisweek.gnome.org/index.xml", "This Week in GNOME", "https://thisweek.gnome.org/", "%a, %d %b %Y %H:%M:%S %Z"],
            ["https://ubuntu.com/blog/feed", "Ubuntu Blog", "https://ubuntu.com/blog", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www-gem.bearblog.dev/feed/", "www-gem words", "https://www-gem.bearblog.dev/", "%Y-%m-%dT%H:%M:%S.%f%z"],
            ["https://linuxhint.com/feed/", "Linux Hint", "https://linuxhint.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.linuxuprising.com/feeds/posts/default", "Linux Uprising", "https://www.linuxuprising.com/", "%Y-%m-%dT%H:%M:%S.%f%z"],
            ["https://boilingsteam.com/feed/", "Boiling Steam", "https://boilingsteam.com/", "%a, %d %b %Y %H:%M:%S %z"]]
        }
    },
    "es": {
        "lang": "es",
        "langFull": "Español",
        "websiteDesc": "Agregador de noticias sobre Linux y software libre, sin Javascript",
        "entries": {
            "news": [["https://feeds.feedburner.com/desdelinuxweb", "Desde Linux", "https://desdelinux.net/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://elpinguinotolkiano.wordpress.com/feed/", "El Pingüino Tolkiano", "https://elpinguinotolkiano.wordpress.com", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://h4ckseed.wordpress.com/feed/", "h4ckseed", "https://h4ckseed.wordpress.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://feeds.feedburner.com/LinuxAdictos", "Linux Adictos", "https://www.linuxadictos.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.muylinux.com/feed/", "MuyLinux", "https://www.muylinux.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://victorhckinthefreeworld.com/feed/", "Victorhck in the free world", "https://victorhckinthefreeworld.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://nksistemas.com/feed/", "NKSistemas", "https://nksistemas.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.kdeblog.com/feed", "KDE Blog", "https://www.kdeblog.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.linuxparty.es/?format=feed&type=rss", "LinuxParty", "https://www.linuxparty.es/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://laboratoriolinux.es/?format=feed&type=rss", "Laboratorio Linux", "https://laboratoriolinux.es/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://feeds.feedburner.com/ubunlog", "Ubunlog", "https://ubunlog.com/", "%a, %d %b %Y %H:%M:%S %z"]],
            "videos": [["https://odysee.com/$/rss/@manosymaquinasentrevideos:6", "Manos y Máquinas Entre Vídeos", "https://odysee.com/@manosymaquinasentrevideos:6", "%a, %d %b %Y %H:%M:%S %Z"],
            ["https://fediverse.tv/feeds/videos.xml?videoChannelId=19129", "Atareao (Vídeos)", "https://fediverse.tv/c/atareao/videos", "%a, %d %b %Y %H:%M:%S %Z"],
            ["https://fediverse.tv/feeds/videos.xml?accountId=132878", "MAINKIVI (Vídeos)", "https://fediverse.tv/a/mainkivi/videos", "%a, %d %b %Y %H:%M:%S %Z"],
            ["https://fediverse.tv/feeds/videos.xml?videoChannelId=22590", "Dani Sánchez", "https://fediverse.tv/c/danisanchez.net/videos", "%a, %d %b %Y %H:%M:%S %Z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UC6ImDlcMZukA-pqtIaXqbdA", "Cumpi Linux", "https://cumpi.ga/", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCl8XUDjAOLc7GNKcDp9Nepg", "Locos por Linux", "https://www.youtube.com/@LocosporLinux/videos", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCFRuGs1rZJ4oAaLsAjypt7A", "Desde Linux con Amor", "https://www.youtube.com/@DesdeLinuxConAmor/videos", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCFnFYB2mWAdVwA7Q94AaLPA", "Linux en Casa", "https://www.youtube.com/@LinuxenCasa/videos", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCgErca6xmDIcaHDnVghHk6w", "Nos Gusta Linux", "https://www.youtube.com/@nosgustalinux/videos", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCta4Iy4TzMx8Xo0pwpkbWgg", "PatoJAD", "https://www.youtube.com/@PatoJAD/videos", "%Y-%m-%dT%H:%M:%S%z"]],
            "more": [["https://voidnull.es/rss/", "voidNull", "https://voidnull.es/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.ochobitshacenunbyte.com/feed/", "ochobitshacenunbyte", "https://www.ochobitshacenunbyte.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://podcastlinux.com/feed", "Podcast Linux", "https://podcastlinux.com/", "%a, %d %b %Y %H:%M:%S %Z"],
            ["https://mainkivi.info/wordpress/blog/feed/", "MAINKIVI", "https://mainkivi.info/wordpress/blog/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://ugeek.github.io/feed.xml", "Blog Podcast uGeek", "https://ugeek.github.io/", "%a, %d %b %Y %H:%M:%S %Z"],
            ["https://elblogdelazaro.org/index.xml", "El Blog de Lázaro", "https://elblogdelazaro.org/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://atareao.es/feed/", "Atareao", "https://atareao.es/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://salmorejogeek.com/feed/", "Salmorejo Geek", "https://salmorejogeek.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://elbinario.net/feed/", "Elbinario", "https://elbinario.net/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://ubuntuperonista.blogspot.com/feeds/posts/default", "Ubuntu Peronista", "https://ubuntuperonista.blogspot.com/", "%Y-%m-%dT%H:%M:%S.%f%z"],
            ["https://martinezmartinez.eu/feed/", "Blog de informática", "https://martinezmartinez.eu/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://feeds.feedburner.com/geeklandlinux", "geekland", "https://geekland.eu/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://myblog.clonbg.es/feedClonbg_es.xml", "Blog de Clonbg", "https://myblog.clonbg.es/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://cambiatealinux.com/rss", "Cambiate a Linux", "https://cambiatealinux.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.bujarra.com/feed/", "Blog Bujarra.com", "https://www.bujarra.com/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://56k.es/feed/", "56K", "https://56k.es/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://c3po.website/rss/", "Blog de C3PO", "https://c3po.website/", "%a, %d %b %Y %H:%M:%S %z"],
            ["http://feeds.feedburner.com/UnBrutoConDebian", "Un bruto con Debian", "https://unbrutocondebian.blogspot.com/", "%Y-%m-%dT%H:%M:%S.%f%z"]]
        }
    },
    "de": {
        "lang": "de",
        "langFull": "Deutsch",
        "websiteDesc": "Javascript-freier Linux/Open-Source-Nachrichten-Aggregator",
        "entries": {
            "news": [["https://linuxnews.de/feed/", "LinuxNews", "https://linuxnews.de/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.linux-magazin.de/feed/", "Linux-Magazin", "https://www.linux-magazin.de/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://gnulinux.ch/rss.xml", "GNU/Linux.ch", "https://gnulinux.ch/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.computerbase.de/thema/linux/index.atom", "ComputerBase", "https://www.computerbase.de/thema/linux/", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://holarse.de/rss.xml", "HOLARSE", "https://holarse.de/", "%a, %d %b %Y %H:%M:%S %z"]],
            "videos": [["https://www.youtube.com/feeds/videos.xml?channel_id=UCHZyqB9qHGGGw5QeRVEbQDg", "Linux Guides DE", "https://www.youtube.com/channel/UCHZyqB9qHGGGw5QeRVEbQDg/videos", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCbvvtG9I_hrfSqT9PfXFXtw", "MichlFranken", "https://www.youtube.com/@MichlFranken/videos", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UC1FC90ObOrYdfsPposnbbMQ", "So'n Typ im Internet", "https://www.youtube.com/@SonTypimInternet/videos", "%Y-%m-%dT%H:%M:%S%z"]],
            "more": [["https://www.howtoforge.de/feed/", "HowtoForge", "https://www.howtoforge.de/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://linux-content.org/feed/", "Linux Content", "https://linux-content.org/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://netzpalaver.de/feed/", "Netzpalaver", "https://netzpalaver.de/", "%a, %d %b %Y %H:%M:%S %z"]]
        }
    },
    "fr": {
        "lang": "fr",
        "langFull": "Français",
        "websiteDesc": "Agrégateur de nouvelles Linux/open source sans Javascript.",
        "entries": {
            "news": [["https://www.toolinux.com/spip.php?page=backend", "TOOLinux", "https://www.toolinux.com/", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://linuxfr.org/news.atom", "LinuxFr.org", "https://linuxfr.org/", "%Y-%m-%dT%H:%M:%S%z"]],
            "videos": [["https://www.youtube.com/feeds/videos.xml?channel_id=UCs_AZuYXi6NA9tkdbhjItHQ", "xavki", "https://www.youtube.com/channel/UCs_AZuYXi6NA9tkdbhjItHQ/videos", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCq6OWb0pyhv5qPtCINJgdxA", "LinuxInFrench", "https://www.youtube.com/channel/UCq6OWb0pyhv5qPtCINJgdxA/videos", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UC5M4fqmqLNJaBey0W_ylCSA", "Actualia", "https://www.youtube.com/@Actualia66/videos", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UC7VqJVFvk75-B0uKg4MWfpw", "Cardiac TuX", "https://www.youtube.com/@Cardiacman/videos", "%Y-%m-%dT%H:%M:%S%z"]],
            "more": [["https://www.numetopia.fr/feed/", "Numétopia", "https://www.numetopia.fr/", "%a, %d %b %Y %H:%M:%S %z"]]
        }
    },
    "pt": {
        "lang": "pt",
        "langFull": "Português",
        "websiteDesc": "Agregador de notícias sem Javascript Linux/ fonte aberta",
        "entries": {
            "news": [["https://sempreupdate.com.br/feed/", "SempreUpdate", "https://sempreupdate.com.br/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://livreeaberto.com/artigos.rss", "é Livre e Aberto", "https://livreeaberto.com/", "%a, %d %b %Y %H:%M:%S %z"]],
            "videos": [["https://odysee.com/$/rss/@livreeaberto:f", "é Livre e Aberto (Videos)", "https://odysee.com/@livreeaberto:f", "%a, %d %b %Y %H:%M:%S %Z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCEf5U1dB5a2e2S-XUlnhxSA", "Diolinux (Videos)", "https://www.youtube.com/@Diolinux/videos", "%Y-%m-%dT%H:%M:%S%z"],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UC-As6gR1nl8nxcyJck20u3w", "Zer01TI", "https://www.youtube.com/@Zer01TI/videos", "%Y-%m-%dT%H:%M:%S%z"]],
            "more": [["https://diolinux.com.br/feed", "Diolinux", "https://diolinux.com.br/", "%a, %d %b %Y %H:%M:%S %z"],
            ["https://www.edivaldobrito.com.br/feed/", "Blog do Edivaldo", "https://www.edivaldobrito.com.br/", "%a, %d %b %Y %H:%M:%S %z"]]
        }
    },
    "jp": {
        "lang": "jp",
        "langFull": "日本語",
        "websiteDesc": "JavaScriptを使用しないLinuxおよびフリーソフトウェアニュースアグリゲーター",
        "entries": {
            "news": [["https://joho-todai.com/pinterest-rss/", "Joho no Todai", "https://joho-todai.com/", "%a, %d %b %Y %H:%M:%S %Z"]],
            "videos": [],
            "more": []
        }
    }
}

# Si OUTPUT_DIR está definido se escribe en local y no se sube nada a S3
OUTPUT_DIR = os.environ.get("OUTPUT_DIR")
BUCKET = "news.rs1.es"
WORK_DIR = OUTPUT_DIR or "/tmp"

SITE_NAME = "RS1 Linux & Open Source News"

# Orden de los idiomas en la barra: los 3 primeros visibles, el resto en el menú "..."
LANGUAGES = ["en", "es", "de", "fr", "pt", "jp"]
LANGUAGES_VISIBLE = LANGUAGES[:3]
LANGUAGES_HIDDEN = LANGUAGES[3:]

# Una entrada por sección: carpeta de salida, etiqueta de la barra y prefijo del <title>
SECTIONS = {
    "news":   {"dir": "",        "label": "NEWS",   "title": None},
    "videos": {"dir": "videos/", "label": "VIDEOS", "title": "Videos"},
    "more":   {"dir": "more/",   "label": "MORE",   "title": "More"},
}

FOOTER = """<footer>
<a href="/"><h2>%s</h2></a>
<div class="footer-content">
<div>
<p>Javascript-free Linux/open source news aggregator.</p>
<p>Linux is a registered trademark of Linus Torvalds.</p>
</div>
</div>
</footer>
</body>
</html>""" % SITE_NAME



# ---------- Feeds ----------

def entryDate(entry, author, parseDate):
    """Fecha de la entrada: la que normaliza feedparser y, si falta, el formato manual del feed."""
    field = "updated" if author in ["DistroWatch", "LWN.net"] else "published"
    parsed = entry.get(field + "_parsed")
    if parsed:
        return datetime.datetime(*parsed[:6], tzinfo=datetime.timezone.utc)
    return datetime.datetime.strptime(entry.get(field, ""), parseDate)

def parseFeed(url, author, homeURL, parseDate):
    entries = []
    d = feedparser.parse(url)
    for entry in d.entries:
        try:
            dt = entryDate(entry, author, parseDate)
        except ValueError:
            print("%s: invalid date in %s" % (author, entry.get("link")))
            continue
        entries.append([entry.title, entry.link, dt.isoformat(), author, homeURL, dt.timestamp()])
    return entries

def parseFeedSafe(feed):
    """Descarga un feed con timeout; un feed roto no debe afectar al resto."""
    try:
        return func_timeout.func_timeout(10, parseFeed, args=tuple(feed))
    except func_timeout.FunctionTimedOut:
        print("%s: timeout" % feed[1])
    except Exception as e:
        print("%s: %s" % (feed[1], e))
    return []

def sortFeeds(feed):
    return sorted(feed, key=lambda entry: entry[5], reverse=True)

def limitFeeds(feed):
    return feed[0:150]

def uploadFileS3(localFile):
    import boto3
    boto3.resource('s3').Bucket(BUCKET).upload_file(WORK_DIR + '/' + localFile, localFile, ExtraArgs={'ContentType': 'text/html'})


# ---------- HTML ----------

def sectionUrl(lang, section):
    """URL absoluta de una sección en un idioma: /, /videos/, /es/more/..."""
    prefix = "/" if lang == "en" else "/%s/" % lang
    return prefix + SECTIONS[section]["dir"]

def pageTitle(section, lang):
    sectionTitle = SECTIONS[section]["title"]
    langFull = strings[lang]["langFull"]
    if sectionTitle is None:
        prefix = "" if lang == "en" else "%s - " % langFull
    else:
        prefix = "%s - " % sectionTitle if lang == "en" else "%s (%s) - " % (sectionTitle, langFull)
    return prefix + SITE_NAME

def barItem(cssClass, href, text, active):
    classes = cssClass + (" item-active" if active else "")
    return '<div class="%s">\n<a href="%s">%s</a>\n</div>\n' % (classes, href, text)

def createFilterBar(section, lang):
    def langItem(code):
        return barItem("language-bar-item", sectionUrl(code, section), code.upper(), code == lang)

    topics = "".join(
        barItem("topic-bar-item", sectionUrl(lang, name), info["label"], name == section)
        for name, info in SECTIONS.items()
    )
    return (
        '<div class="filter-bar"><div class="language-bar">\n'
        '<div class="language-bar-title"><span>Language:</span></div>'
        + "".join(langItem(c) for c in LANGUAGES_VISIBLE)
        + '<div class="language-bar-item other-div">\n<span>...</span>\n<div class="other-languages">\n'
        '<div class="language-bar-item no-hover">\n<span>&nbsp;</span>\n</div>\n'
        + "".join(langItem(c) for c in LANGUAGES_HIDDEN)
        + '</div>\n</div>\n</div>\n'
        '<div class="topic-bar">\n<div class="topic-bar-title">\n<span>Topic:</span>\n</div>\n'
        + topics
        + '</div>\n</div>'
    )

def createHeader(section, lang):
    return (
        '<!DOCTYPE html>\n'
        '<html lang="%s">\n'
        '<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<meta name="description" content="%s">\n'
        '<title>%s</title><link rel="shortcut icon" href="/favicon.png" type="image/png">\n'
        '<link rel="stylesheet" href="/main.min.css">\n</head>\n'
        '<body>\n<div class="topbar">\n<div class="main-title">\n<a href="/"><h1>%s</h1></a>\n</div>\n'
        '<div class="topbar-links"><div class="topbar-link-item"><a href="/about.html">About</a>\n</div>\n</div>\n</div>\n'
    ) % (strings[lang]["lang"], strings[lang]["websiteDesc"], pageTitle(section, lang), SITE_NAME)

def createEntries(file, entries):
    file.write("<div class=\"post-list\">\n")
    for entry in entries:
        dtentry = datetime.datetime.fromisoformat(entry[2])
        tz = pytz.timezone("UTC")
        dtentry = dtentry.astimezone(tz)
        file.write("<div class=\"post-item\">\n")
        file.write("<a target=\"_blank\" rel=\"noopener\" href=\"%s\">\n" % html.escape(entry[1], quote=True))
        file.write("<h2>%s</h2>\n" % html.escape(entry[0]))
        file.write("</a>\n")
        file.write("<a target=\"_blank\" rel=\"noopener\" href=\"%s\">%s</a>\n" % (html.escape(entry[4], quote=True), html.escape(entry[3])))
        file.write("<time datetime=\"%s\">%s</time>\n" % (entry[2], dtentry.strftime('%a, %d %b %Y %H:%M')))
        file.write("</div>\n")
    file.write("</div>\n")

def createPage(file, entries, section, lang):
    file.write(createHeader(section, lang))
    file.write(createFilterBar(section, lang))
    createEntries(file, entries)
    file.write(FOOTER)


# ---------- Proceso principal ----------

def mainProcess(section, feedInfo, lang):
    path = ("" if lang == "en" else lang + "/") + SECTIONS[section]["dir"]
    with ThreadPoolExecutor(max_workers=16) as pool:
        receivedFeeds = [e for result in pool.map(parseFeedSafe, feedInfo) for e in result]
    print("- %s feeds parsed -" % section)

    # Sin ninguna entrada (p. ej. corte de red) se conserva la página anterior en S3
    if feedInfo and not receivedFeeds:
        print("%s: no entries, page not updated" % path)
        return False

    joinFeedSorted = limitFeeds(sortFeeds(receivedFeeds))

    os.makedirs(WORK_DIR + "/" + path, exist_ok=True)
    with open(WORK_DIR + "/" + path + "index.html", "w") as htmlFile:
        createPage(htmlFile, joinFeedSorted, section, lang)
    print(path + "index.html saved")
    if not OUTPUT_DIR:
        uploadFileS3(path + "index.html")
    return True

def main():
    failed = []
    for lang in LANGUAGES:
        for section in SECTIONS:
            if not mainProcess(section, strings[lang]["entries"][section], lang):
                failed.append("%s/%s" % (lang, section))
    # Falla al final, tras generar el resto, para que Lambda registre el error
    if failed:
        raise RuntimeError("Pages not updated: " + ", ".join(failed))

if __name__ == "__main__":
    main()
