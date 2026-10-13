import feedparser
import datetime
import os
import pytz
import func_timeout
import boto3

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
            ["https://www.linuxinsider.com/rss-feed", "LinuxInsider", "https://www.linuxinsider.com/", "%a, %d %b %Y %H:%M:%S %z"]],
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

s3 = boto3.resource('s3')

def parseFeed(url, author, homeURL, parseDate, globalFeed):
    d = feedparser.parse(url)
    for entry in d.entries:
        if author in ["DistroWatch", "LWN.net"]:
            entry.published = entry.updated
        dt = 0
        try:
            dt = datetime.datetime.strptime(entry.published, parseDate)
        except ValueError:
            print(entry.published + " does not follow " + parseDate)
            continue
        entry.published = dt.isoformat()
        globalFeed.append([entry.title, entry.link, entry.published, author, homeURL, dt.timestamp()])

def testParse(url):
    d = feedparser.parse(url)
    for entry in d.entries:
        print(entry.title, entry.link, entry.published)

def sortFeeds(feed):
    return sorted(feed, key=lambda entry: entry[5], reverse=True)

def limitFeeds(feed):
    return feed[0:150]

def uploadFileS3(localFile):
    s3.Bucket('news.rs1.es').upload_file('/tmp/' + localFile, localFile, ExtraArgs={'ContentType': 'text/html'})

def createEntries(file, entries):
    file.write("<div class=\"post-list\">\n")
    for entry in entries:
        dtentry = datetime.datetime.fromisoformat(entry[2])
        tz = pytz.timezone("UTC")
        dtentry = dtentry.astimezone(tz)
        file.write("<div class=\"post-item\">\n")
        file.write("<a target=\"_blank\" href=\"%s\">\n" %entry[1])
        file.write("<h2>%s</h2>\n" %entry[0])
        file.write("</a>\n")
        file.write("<a target=\"_blank\" href=\"%s\">%s</a>\n" %(entry[4], entry[3]))
        file.write("<time datetime=\"%s\">%s</time>\n" %(entry[2], dtentry.strftime('%a, %d %b %Y %H:%M')))
        file.write("</div>\n")
    file.write("</div>\n")

def createHome(file, entries, lang):
    file.write("<!DOCTYPE html>\n")
    file.write("<html lang=\"%s\">\n" %strings[lang]["lang"])
    file.write("<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n<meta name=\"description\" content=\"%s\">\n" %strings[lang]["websiteDesc"])
    if lang != "en":
        file.write("<title>%s - RS1 Linux News</title><link rel=\"shortcut icon\" href=\"/favicon.png\" type=\"image/png\">\n<link rel=\"stylesheet\" href=\"/main.css\">\n</head>\n" %strings[lang]["langFull"])
    else:
        file.write("<title>RS1 Linux News</title><link rel=\"shortcut icon\" href=\"/favicon.png\" type=\"image/png\">\n<link rel=\"stylesheet\" href=\"/main.css\">\n</head>\n")
    file.write("<body>\n<div class=\"topbar\">\n<div class=\"main-title\">\n<a href=\"/\"><h1>RS1 Linux News</h1></a>\n</div>\n<div class=\"topbar-links\"><div class=\"topbar-link-item\"><a href=\"/about.html\">About</a>\n</div>\n</div>\n</div>\n<div class=\"filter-bar\"><div class=\"language-bar\">\n<div class=\"language-bar-title\"><span>Language:</span></div>")
    if lang == "en":
        temp1 = """<div class="language-bar-item item-active">
        <a href="/">EN</a>
        </div>
        <div class="language-bar-item">
        <a href="/es/">ES</a>
        </div>
        <div class="language-bar-item">
        <a href="/de/">DE</a>
        </div>
        <div class="language-bar-item other-div">
        <span>...</span>
        <div class="other-languages">
        <div class="language-bar-item no-hover">
        <span>&nbsp;</span>
        </div>
        <div class="language-bar-item">
        <a href="/fr/">FR</a>
        </div>
        <div class="language-bar-item">
        <a href="/pt/">PT</a>
        </div>
        <div class="language-bar-item">
        <a href="/jp/">JP</a>
        </div>
        </div>
        </div>
        </div>
        <div class="topic-bar">
        <div class="topic-bar-title">
        <span>Topic:</span>
        </div>
        <div class="topic-bar-item item-active">
        <a href="/">NEWS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/videos/">VIDEOS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/more/">MORE</a>
        </div>
        </div>
        </div>"""
    elif lang == "es":
        temp1 = """<div class="language-bar-item">
        <a href="/">EN</a>
        </div>
        <div class="language-bar-item item-active">
        <a href="/es/">ES</a>
        </div>
        <div class="language-bar-item">
        <a href="/de/">DE</a>
        </div>
        <div class="language-bar-item other-div">
        <span>...</span>
        <div class="other-languages">
        <div class="language-bar-item no-hover">
        <span>&nbsp;</span>
        </div>
        <div class="language-bar-item">
        <a href="/fr/">FR</a>
        </div>
        <div class="language-bar-item">
        <a href="/pt/">PT</a>
        </div>
        <div class="language-bar-item">
        <a href="/jp/">JP</a>
        </div>
        </div>
        </div>
        </div>
        <div class="topic-bar">
        <div class="topic-bar-title">
        <span>Topic:</span>
        </div>
        <div class="topic-bar-item item-active">
        <a href="/es/">NEWS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/es/videos/">VIDEOS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/es/more/">MORE</a>
        </div>
        </div>
        </div>"""
    elif lang == "de":
        temp1 = """<div class="language-bar-item">
        <a href="/">EN</a>
        </div>
        <div class="language-bar-item">
        <a href="/es/">ES</a>
        </div>
        <div class="language-bar-item item-active">
        <a href="/de/">DE</a>
        </div>
        <div class="language-bar-item other-div">
        <span>...</span>
        <div class="other-languages">
        <div class="language-bar-item no-hover">
        <span>&nbsp;</span>
        </div>
        <div class="language-bar-item">
        <a href="/fr/">FR</a>
        </div>
        <div class="language-bar-item">
        <a href="/pt/">PT</a>
        </div>
        <div class="language-bar-item">
        <a href="/jp/">JP</a>
        </div>
        </div>
        </div>
        </div>
        <div class="topic-bar">
        <div class="topic-bar-title">
        <span>Topic:</span>
        </div>
        <div class="topic-bar-item item-active">
        <a href="/de/">NEWS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/de/videos/">VIDEOS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/de/more/">MORE</a>
        </div>
        </div>
        </div>"""
    elif lang == "fr":
        temp1 = """<div class="language-bar-item">
        <a href="/">EN</a>
        </div>
        <div class="language-bar-item">
        <a href="/es/">ES</a>
        </div>
        <div class="language-bar-item">
        <a href="/de/">DE</a>
        </div>
        <div class="language-bar-item other-div">
        <span>...</span>
        <div class="other-languages">
        <div class="language-bar-item no-hover">
        <span>&nbsp;</span>
        </div>
        <div class="language-bar-item item-active">
        <a href="/fr/">FR</a>
        </div>
        <div class="language-bar-item">
        <a href="/pt/">PT</a>
        </div>
        <div class="language-bar-item">
        <a href="/jp/">JP</a>
        </div>
        </div>
        </div>
        </div>
        <div class="topic-bar">
        <div class="topic-bar-title">
        <span>Topic:</span>
        </div>
        <div class="topic-bar-item item-active">
        <a href="/fr/">NEWS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/fr/videos/">VIDEOS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/fr/more/">MORE</a>
        </div>
        </div>
        </div>"""
    elif lang == "pt":
        temp1 = """<div class="language-bar-item">
        <a href="/">EN</a>
        </div>
        <div class="language-bar-item">
        <a href="/es/">ES</a>
        </div>
        <div class="language-bar-item">
        <a href="/de/">DE</a>
        </div>
        <div class="language-bar-item other-div">
        <span>...</span>
        <div class="other-languages">
        <div class="language-bar-item no-hover">
        <span>&nbsp;</span>
        </div>
        <div class="language-bar-item>
        <a href="/fr/">FR</a>
        </div>
        <div class="language-bar-item item-active">
        <a href="/pt/">PT</a>
        </div>
        <div class="language-bar-item">
        <a href="/jp/">JP</a>
        </div>
        </div>
        </div>
        </div>
        <div class="topic-bar">
        <div class="topic-bar-title">
        <span>Topic:</span>
        </div>
        <div class="topic-bar-item item-active">
        <a href="/pt/">NEWS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/pt/videos/">VIDEOS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/pt/more/">MORE</a>
        </div>
        </div>
        </div>"""
    elif lang == "jp":
        temp1 = """<div class="language-bar-item">
        <a href="/">EN</a>
        </div>
        <div class="language-bar-item">
        <a href="/es/">ES</a>
        </div>
        <div class="language-bar-item">
        <a href="/de/">DE</a>
        </div>
        <div class="language-bar-item other-div">
        <span>...</span>
        <div class="other-languages">
        <div class="language-bar-item no-hover">
        <span>&nbsp;</span>
        </div>
        <div class="language-bar-item>
        <a href="/fr/">FR</a>
        </div>
        <div class="language-bar-item">
        <a href="/pt/">PT</a>
        </div>
        <div class="language-bar-item item-active">
        <a href="/jp/">JP</a>
        </div>
        </div>
        </div>
        </div>
        <div class="topic-bar">
        <div class="topic-bar-title">
        <span>Topic:</span>
        </div>
        <div class="topic-bar-item item-active">
        <a href="/jp/">NEWS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/jp/videos/">VIDEOS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/jp/more/">MORE</a>
        </div>
        </div>
        </div>"""
    file.write(temp1)
    createEntries(file, entries)
    temp2 = """<footer>
    <a href="/"><h2>RS1 Linux News</h2></a>
    <div class="footer-content">
    <div>
    <p>Javascript-free Linux/open source news aggregator.</p>
    <p>Linux is a registered trademark of Linus Torvalds.</p>
    </div>
    </div>
    </footer>
    </body>
    </html>"""
    file.write(temp2)

def createVideos(file, entries, lang):
    file.write("<!DOCTYPE html>\n")
    file.write("<html lang=\"%s\">\n" %strings[lang]["lang"])
    file.write("<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n<meta name=\"description\" content=\"%s\">\n" %strings[lang]["websiteDesc"])
    if lang != "en":
        file.write("<title>Videos (%s) - RS1 Linux News</title><link rel=\"shortcut icon\" href=\"/favicon.png\" type=\"image/png\">\n<link rel=\"stylesheet\" href=\"/main.css\">\n</head>\n" %strings[lang]["langFull"])
    else:
        file.write("<title>Videos - RS1 Linux News</title><link rel=\"shortcut icon\" href=\"/favicon.png\" type=\"image/png\">\n<link rel=\"stylesheet\" href=\"/main.css\">\n</head>\n")
    file.write("<body>\n<div class=\"topbar\">\n<div class=\"main-title\">\n<a href=\"/\"><h1>RS1 Linux News</h1></a>\n</div>\n<div class=\"topbar-links\"><div class=\"topbar-link-item\"><a href=\"/about.html\">About</a>\n</div>\n</div>\n</div>\n<div class=\"filter-bar\"><div class=\"language-bar\">\n<div class=\"language-bar-title\"><span>Language:</span></div>")
    if lang == "en":
        temp1 = """<div class="language-bar-item item-active">
        <a href="/">EN</a>
        </div>
        <div class="language-bar-item">
        <a href="/es/">ES</a>
        </div>
        <div class="language-bar-item">
        <a href="/de/">DE</a>
        </div>
        <div class="language-bar-item other-div">
        <span>...</span>
        <div class="other-languages">
        <div class="language-bar-item no-hover">
        <span>&nbsp;</span>
        </div>
        <div class="language-bar-item">
        <a href="/fr/">FR</a>
        </div>
        <div class="language-bar-item">
        <a href="/pt/">PT</a>
        </div>
        <div class="language-bar-item">
        <a href="/jp/">JP</a>
        </div>
        </div>
        </div>
        </div>
        <div class="topic-bar">
        <div class="topic-bar-title">
        <span>Topic:</span>
        </div>
        <div class="topic-bar-item">
        <a href="/">NEWS</a>
        </div>
        <div class="topic-bar-item item-active">
        <a href="/videos/">VIDEOS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/more/">MORE</a>
        </div>
        </div>
        </div>"""
    elif lang == "es":
        temp1 = """<div class="language-bar-item">
        <a href="/">EN</a>
        </div>
        <div class="language-bar-item item-active">
        <a href="/es/">ES</a>
        </div>
        <div class="language-bar-item">
        <a href="/de/">DE</a>
        </div>
        <div class="language-bar-item other-div">
        <span>...</span>
        <div class="other-languages">
        <div class="language-bar-item no-hover">
        <span>&nbsp;</span>
        </div>
        <div class="language-bar-item">
        <a href="/fr/">FR</a>
        </div>
        <div class="language-bar-item">
        <a href="/pt/">PT</a>
        </div>
        <div class="language-bar-item">
        <a href="/jp/">JP</a>
        </div>
        </div>
        </div>
        </div>
        <div class="topic-bar">
        <div class="topic-bar-title">
        <span>Topic:</span>
        </div>
        <div class="topic-bar-item">
        <a href="/es/">NEWS</a>
        </div>
        <div class="topic-bar-item item-active">
        <a href="/es/videos/">VIDEOS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/es/more/">MORE</a>
        </div>
        </div>
        </div>"""
    elif lang == "de":
        temp1 = """<div class="language-bar-item">
        <a href="/">EN</a>
        </div>
        <div class="language-bar-item">
        <a href="/es/">ES</a>
        </div>
        <div class="language-bar-item item-active">
        <a href="/de/">DE</a>
        </div>
        <div class="language-bar-item other-div">
        <span>...</span>
        <div class="other-languages">
        <div class="language-bar-item no-hover">
        <span>&nbsp;</span>
        </div>
        <div class="language-bar-item">
        <a href="/fr/">FR</a>
        </div>
        <div class="language-bar-item">
        <a href="/pt/">PT</a>
        </div>
        <div class="language-bar-item">
        <a href="/jp/">JP</a>
        </div>
        </div>
        </div>
        </div>
        <div class="topic-bar">
        <div class="topic-bar-title">
        <span>Topic:</span>
        </div>
        <div class="topic-bar-item">
        <a href="/de/">NEWS</a>
        </div>
        <div class="topic-bar-item item-active">
        <a href="/de/videos/">VIDEOS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/de/more/">MORE</a>
        </div>
        </div>
        </div>"""
    elif lang == "fr":
        temp1 = """<div class="language-bar-item">
        <a href="/">EN</a>
        </div>
        <div class="language-bar-item">
        <a href="/es/">ES</a>
        </div>
        <div class="language-bar-item">
        <a href="/de/">DE</a>
        </div>
        <div class="language-bar-item other-div">
        <span>...</span>
        <div class="other-languages">
        <div class="language-bar-item no-hover">
        <span>&nbsp;</span>
        </div>
        <div class="language-bar-item item-active">
        <a href="/fr/">FR</a>
        </div>
        <div class="language-bar-item">
        <a href="/pt/">PT</a>
        </div>
        <div class="language-bar-item">
        <a href="/jp/">JP</a>
        </div>
        </div>
        </div>
        </div>
        <div class="topic-bar">
        <div class="topic-bar-title">
        <span>Topic:</span>
        </div>
        <div class="topic-bar-item">
        <a href="/fr/">NEWS</a>
        </div>
        <div class="topic-bar-item item-active">
        <a href="/fr/videos/">VIDEOS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/fr/more/">MORE</a>
        </div>
        </div>
        </div>"""
    elif lang == "pt":
        temp1 = """<div class="language-bar-item">
        <a href="/">EN</a>
        </div>
        <div class="language-bar-item">
        <a href="/es/">ES</a>
        </div>
        <div class="language-bar-item">
        <a href="/de/">DE</a>
        </div>
        <div class="language-bar-item other-div">
        <span>...</span>
        <div class="other-languages">
        <div class="language-bar-item no-hover">
        <span>&nbsp;</span>
        </div>
        <div class="language-bar-item>
        <a href="/fr/">FR</a>
        </div>
        <div class="language-bar-item item-active">
        <a href="/pt/">PT</a>
        </div>
        <div class="language-bar-item">
        <a href="/jp/">JP</a>
        </div>
        </div>
        </div>
        </div>
        <div class="topic-bar">
        <div class="topic-bar-title">
        <span>Topic:</span>
        </div>
        <div class="topic-bar-item">
        <a href="/pt/">NEWS</a>
        </div>
        <div class="topic-bar-item item-active">
        <a href="/pt/videos/">VIDEOS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/pt/more/">MORE</a>
        </div>
        </div>
        </div>"""
    elif lang == "jp":
        temp1 = """<div class="language-bar-item">
        <a href="/">EN</a>
        </div>
        <div class="language-bar-item">
        <a href="/es/">ES</a>
        </div>
        <div class="language-bar-item">
        <a href="/de/">DE</a>
        </div>
        <div class="language-bar-item other-div">
        <span>...</span>
        <div class="other-languages">
        <div class="language-bar-item no-hover">
        <span>&nbsp;</span>
        </div>
        <div class="language-bar-item>
        <a href="/fr/">FR</a>
        </div>
        <div class="language-bar-item">
        <a href="/pt/">PT</a>
        </div>
        <div class="language-bar-item item-active">
        <a href="/jp/">JP</a>
        </div>
        </div>
        </div>
        </div>
        <div class="topic-bar">
        <div class="topic-bar-title">
        <span>Topic:</span>
        </div>
        <div class="topic-bar-item">
        <a href="/jp/">NEWS</a>
        </div>
        <div class="topic-bar-item item-active">
        <a href="/jp/videos/">VIDEOS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/jp/more/">MORE</a>
        </div>
        </div>
        </div>"""
    file.write(temp1)
    createEntries(file, entries)
    temp2 = """<footer>
    <a href="/"><h2>RS1 Linux News</h2></a>
    <div class="footer-content">
    <div>
    <p>Javascript-free Linux/open source news aggregator.</p>
    <p>Linux is a registered trademark of Linus Torvalds.</p>
    </div>
    </div>
    </footer>
    </body>
    </html>"""
    file.write(temp2)

def createMore(file, entries, lang):
    file.write("<!DOCTYPE html>\n")
    file.write("<html lang=\"%s\">\n" %strings[lang]["lang"])
    file.write("<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n<meta name=\"description\" content=\"%s\">\n" %strings[lang]["websiteDesc"])
    if lang != "en":
        file.write("<title>More (%s) - RS1 Linux News</title><link rel=\"shortcut icon\" href=\"/favicon.png\" type=\"image/png\">\n<link rel=\"stylesheet\" href=\"/main.css\">\n</head>\n" %strings[lang]["langFull"])
    else:
        file.write("<title>More - RS1 Linux News</title><link rel=\"shortcut icon\" href=\"/favicon.png\" type=\"image/png\">\n<link rel=\"stylesheet\" href=\"/main.css\">\n</head>\n")
    file.write("<body>\n<div class=\"topbar\">\n<div class=\"main-title\">\n<a href=\"/\"><h1>RS1 Linux News</h1></a>\n</div>\n<div class=\"topbar-links\"><div class=\"topbar-link-item\"><a href=\"/about.html\">About</a>\n</div>\n</div>\n</div>\n<div class=\"filter-bar\"><div class=\"language-bar\">\n<div class=\"language-bar-title\"><span>Language:</span></div>")
    if lang == "en":
        temp1 = """<div class="language-bar-item item-active">
        <a href="/">EN</a>
        </div>
        <div class="language-bar-item">
        <a href="/es/">ES</a>
        </div>
        <div class="language-bar-item">
        <a href="/de/">DE</a>
        </div>
        <div class="language-bar-item other-div">
        <span>...</span>
        <div class="other-languages">
        <div class="language-bar-item no-hover">
        <span>&nbsp;</span>
        </div>
        <div class="language-bar-item">
        <a href="/fr/">FR</a>
        </div>
        <div class="language-bar-item">
        <a href="/pt/">PT</a>
        </div>
        <div class="language-bar-item">
        <a href="/jp/">JP</a>
        </div>
        </div>
        </div>
        </div>
        <div class="topic-bar">
        <div class="topic-bar-title">
        <span>Topic:</span>
        </div>
        <div class="topic-bar-item">
        <a href="/">NEWS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/videos/">VIDEOS</a>
        </div>
        <div class="topic-bar-item item-active">
        <a href="/more/">MORE</a>
        </div>
        </div>
        </div>"""
    elif lang == "es":
        temp1 = """<div class="language-bar-item">
        <a href="/">EN</a>
        </div>
        <div class="language-bar-item item-active">
        <a href="/es/">ES</a>
        </div>
        <div class="language-bar-item">
        <a href="/de/">DE</a>
        </div>
        <div class="language-bar-item other-div">
        <span>...</span>
        <div class="other-languages">
        <div class="language-bar-item no-hover">
        <span>&nbsp;</span>
        </div>
        <div class="language-bar-item">
        <a href="/fr/">FR</a>
        </div>
        <div class="language-bar-item">
        <a href="/pt/">PT</a>
        </div>
        <div class="language-bar-item">
        <a href="/jp/">JP</a>
        </div>
        </div>
        </div>
        </div>
        <div class="topic-bar">
        <div class="topic-bar-title">
        <span>Topic:</span>
        </div>
        <div class="topic-bar-item">
        <a href="/es/">NEWS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/es/videos/">VIDEOS</a>
        </div>
        <div class="topic-bar-item item-active">
        <a href="/es/more/">MORE</a>
        </div>
        </div>
        </div>"""
    elif lang == "de":
        temp1 = """<div class="language-bar-item">
        <a href="/">EN</a>
        </div>
        <div class="language-bar-item">
        <a href="/es/">ES</a>
        </div>
        <div class="language-bar-item item-active">
        <a href="/de/">DE</a>
        </div>
        <div class="language-bar-item other-div">
        <span>...</span>
        <div class="other-languages">
        <div class="language-bar-item no-hover">
        <span>&nbsp;</span>
        </div>
        <div class="language-bar-item">
        <a href="/fr/">FR</a>
        </div>
        <div class="language-bar-item">
        <a href="/pt/">PT</a>
        </div>
        <div class="language-bar-item">
        <a href="/jp/">JP</a>
        </div>
        </div>
        </div>
        </div>
        <div class="topic-bar">
        <div class="topic-bar-title">
        <span>Topic:</span>
        </div>
        <div class="topic-bar-item">
        <a href="/de/">NEWS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/de/videos/">VIDEOS</a>
        </div>
        <div class="topic-bar-item item-active">
        <a href="/de/more/">MORE</a>
        </div>
        </div>
        </div>"""
    elif lang == "fr":
        temp1 = """<div class="language-bar-item">
        <a href="/">EN</a>
        </div>
        <div class="language-bar-item">
        <a href="/es/">ES</a>
        </div>
        <div class="language-bar-item">
        <a href="/de/">DE</a>
        </div>
        <div class="language-bar-item other-div">
        <span>...</span>
        <div class="other-languages">
        <div class="language-bar-item no-hover">
        <span>&nbsp;</span>
        </div>
        <div class="language-bar-item item-active">
        <a href="/fr/">FR</a>
        </div>
        <div class="language-bar-item">
        <a href="/pt/">PT</a>
        </div>
        <div class="language-bar-item">
        <a href="/jp/">JP</a>
        </div>
        </div>
        </div>
        </div>
        <div class="topic-bar">
        <div class="topic-bar-title">
        <span>Topic:</span>
        </div>
        <div class="topic-bar-item">
        <a href="/fr/">NEWS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/fr/videos/">VIDEOS</a>
        </div>
        <div class="topic-bar-item item-active">
        <a href="/fr/more/">MORE</a>
        </div>
        </div>
        </div>"""
    elif lang == "pt":
        temp1 = """<div class="language-bar-item">
        <a href="/">EN</a>
        </div>
        <div class="language-bar-item">
        <a href="/es/">ES</a>
        </div>
        <div class="language-bar-item">
        <a href="/de/">DE</a>
        </div>
        <div class="language-bar-item other-div">
        <span>...</span>
        <div class="other-languages">
        <div class="language-bar-item no-hover">
        <span>&nbsp;</span>
        </div>
        <div class="language-bar-item>
        <a href="/fr/">FR</a>
        </div>
        <div class="language-bar-item item-active">
        <a href="/pt/">PT</a>
        </div>
        <div class="language-bar-item">
        <a href="/jp/">JP</a>
        </div>
        </div>
        </div>
        </div>
        <div class="topic-bar">
        <div class="topic-bar-title">
        <span>Topic:</span>
        </div>
        <div class="topic-bar-item">
        <a href="/pt/">NEWS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/pt/videos/">VIDEOS</a>
        </div>
        <div class="topic-bar-item item-active">
        <a href="/pt/more/">MORE</a>
        </div>
        </div>
        </div>"""
    elif lang == "jp":
        temp1 = """<div class="language-bar-item">
        <a href="/">EN</a>
        </div>
        <div class="language-bar-item">
        <a href="/es/">ES</a>
        </div>
        <div class="language-bar-item">
        <a href="/de/">DE</a>
        </div>
        <div class="language-bar-item other-div">
        <span>...</span>
        <div class="other-languages">
        <div class="language-bar-item no-hover">
        <span>&nbsp;</span>
        </div>
        <div class="language-bar-item>
        <a href="/fr/">FR</a>
        </div>
        <div class="language-bar-item">
        <a href="/pt/">PT</a>
        </div>
        <div class="language-bar-item item-active">
        <a href="/jp/">JP</a>
        </div>
        </div>
        </div>
        </div>
        <div class="topic-bar">
        <div class="topic-bar-title">
        <span>Topic:</span>
        </div>
        <div class="topic-bar-item">
        <a href="/jp/">NEWS</a>
        </div>
        <div class="topic-bar-item">
        <a href="/jp/videos/">VIDEOS</a>
        </div>
        <div class="topic-bar-item item-active">
        <a href="/jp/more/">MORE</a>
        </div>
        </div>
        </div>"""
    file.write(temp1)
    createEntries(file, entries)
    temp2 = """<footer>
    <a href="/"><h2>RS1 Linux News</h2></a>
    <div class="footer-content">
    <div>
    <p>Javascript-free Linux/open source news aggregator.</p>
    <p>Linux is a registered trademark of Linus Torvalds.</p>
    </div>
    </div>
    </footer>
    </body>
    </html>"""
    file.write(temp2)

def mainProcess(section, feedInfo, path, lang):
    receivedFeeds = []
    for feed in feedInfo:
        print(feed[1])
        try:
            func_timeout.func_timeout(10, parseFeed, args=(feed[0], feed[1], feed[2], feed[3], receivedFeeds))
        except func_timeout.FunctionTimedOut:
            pass
    print("- %s feeds parsed -" %section)

    joinFeedSorted = sortFeeds(receivedFeeds)
    joinFeedSorted = limitFeeds(joinFeedSorted)

    if os.path.exists("/tmp/" + path) == False:
        os.makedirs("/tmp/" + path)

    htmlFile = open("/tmp/" + path + "index.html", "w")
    if section == "news":
        createHome(htmlFile, joinFeedSorted, lang)
    elif section == "videos":
        createVideos(htmlFile, joinFeedSorted, lang)
    elif section == "more":
        createMore(htmlFile, joinFeedSorted, lang)
    htmlFile.close()
    print(path + "index.html saved")
    uploadFileS3(path + "index.html")

mainProcess("news", strings["en"]["entries"]["news"], "", "en")
mainProcess("videos", strings["en"]["entries"]["videos"], "videos/", "en")
mainProcess("more", strings["en"]["entries"]["more"], "more/", "en")

for i in ["es", "de", "fr", "pt", "jp"]:
    mainProcess("news", strings[i]["entries"]["news"], i + "/", i)
    mainProcess("videos", strings[i]["entries"]["videos"], i + "/videos/", i)
    mainProcess("more", strings[i]["entries"]["more"], i + "/more/", i)
