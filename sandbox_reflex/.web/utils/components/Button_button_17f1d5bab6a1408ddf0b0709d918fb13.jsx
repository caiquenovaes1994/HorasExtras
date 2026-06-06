
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Button as RadixThemesButton} from "@radix-ui/themes"
import {EventLoopContext} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Button_button_17f1d5bab6a1408ddf0b0709d918fb13 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_click_2832818f52e3db9a155c0ca8a8d746b4 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.aceitar_termos_lgpd", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{css:({ ["width"] : "100%" }),onClick:on_click_2832818f52e3db9a155c0ca8a8d746b4,size:"3"},children)
    )
});
