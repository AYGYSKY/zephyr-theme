window.__ModuleLoader__.load({
  id: 'dsh-zephyr-theme',
  factory() {
    // 正常情况下 host 已经把 CSS 注入到 <head>（首帧就是主题色）。
    // 这里只做兜底：没有 webServer 的宿主、或注入被跳过时，拉一份外链样式。
    const HREF = '/zephyr-theme.css';
    const MARK = '/*!zephyr-theme*/';

    function alreadyInjected() {
      try {
        const styles = Array.from(document.querySelectorAll('style'));
        if (styles.some((node) => (node.textContent || '').includes(MARK))) return true;
        return Boolean(document.querySelector('link[data-zephyr-theme]'));
      } catch (error) {
        return false;
      }
    }

    return {
      apply(ctx) {
        ctx.effect(() => {
          const root = document.documentElement;
          let link = null;

          if (!alreadyInjected()) {
            link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = HREF;
            link.setAttribute('data-zephyr-theme', '');
            document.head.appendChild(link);
          }

          root.setAttribute('data-zephyr-ui', '');

          return () => {
            if (link) link.remove();
            root.removeAttribute('data-zephyr-ui');
          };
        });
      },
    };
  },
});
