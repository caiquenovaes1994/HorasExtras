
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Text as RadixThemesText} from "@radix-ui/themes"
import {EventLoopContext} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Text_text_d282113f5845f9f0368ae6889e0da68b = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_click_0688bdbe68194d253ec82a2962127057 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.toggle_policy", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesText,{as:"span",css:({ ["cursor"] : "pointer", ["textDecoration"] : "underline", ["color"] : "var(--blue-11)" }),onClick:on_click_0688bdbe68194d253ec82a2962127057,weight:"bold"},children)
    )
});
