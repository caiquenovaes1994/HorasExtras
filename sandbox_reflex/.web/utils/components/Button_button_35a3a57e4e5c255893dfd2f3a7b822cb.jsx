
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Button as RadixThemesButton} from "@radix-ui/themes"
import {EventLoopContext} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Button_button_35a3a57e4e5c255893dfd2f3a7b822cb = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_click_339426a603bbc2f5dcc6df07b0bf911a = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_usuarios____usuario_state.close_modal", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{color:"gray",css:({ ["cursor"] : "pointer" }),onClick:on_click_339426a603bbc2f5dcc6df07b0bf911a,variant:"soft"},children)
    )
});
